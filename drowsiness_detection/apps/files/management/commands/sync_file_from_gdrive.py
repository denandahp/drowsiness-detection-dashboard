import cv2
import io
import os
import shutil
import zipfile
from django.conf import settings
from django.core.management.base import BaseCommand

from drowsiness_detection.apps.cameras.model import Camera
from drowsiness_detection.apps.files.model import RecordingFile
from drowsiness_detection.apps.users.model import User
from drowsiness_detection.core.services.google import googledrive_service
from drowsiness_detection.core.services.twilio import send_whatsapp

from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        users = User.objects.all()
        users_files = {}

        for user in users:
            service = googledrive_service(user, 'cron')
            if not service: continue
            files = self.get_file_gdrive(service)

            existingFiles = RecordingFile.objects.filter(
                type=RecordingFile.TYPE.googledrive,
                created_by=user).only('google_drive_id', 'name', 'id')
            existingGdriveIds = list(map(lambda file: file.google_drive_id, existingFiles))
            existingCameras = Camera.objects.filter().only('name', 'id')
            existingFilesObj = {}
            existingCamerasObj = {}
            for extFile in existingFiles: existingFilesObj[extFile.google_drive_id] = extFile
            for extCamera in existingCameras: existingCamerasObj[extCamera.name] = extCamera

            userFileList = []
            userDelFileList = []
            for file in files:
                camera = self.camera_object(file, existingCamerasObj, user) # Get camera object
                if(file.get('mimeType') in ['video/mpeg', 'video/mp4', 'image/jpeg']):
                    mimeType = None
                    if file.get('mimeType') in ['video/mpeg', 'video/mp4']: mimeType = RecordingFile.MIMETYPE.video
                    else: mimeType = RecordingFile.MIMETYPE.image

                    if file.get('id') not in existingGdriveIds:
                        createFile = RecordingFile.objects.create(
                            name=file.get('name'),
                            created=file.get('createdTime'),
                            updated=file.get('modifiedTime'),
                            created_by=user,
                            modified_by=user,
                            url=file.get('webViewLink').replace("view", "preview"),
                            google_drive_id=file.get('id'),
                            type=RecordingFile.TYPE.googledrive,
                            is_from_gdrive=True,
                            mimetype=mimeType,
                            camera=camera
                        )
                        userFileList.append(createFile)
                    else:
                    # TODO: need discussion about update file if exist
                    #     updateFile = existingFilesObj[file.get('id')]
                    #     updateFile.name = file.get('name')
                    #     updateFile.url = file.get('webViewLink').replace("view", "preview")
                    #     updateFile.camera = camera
                    #     updateFile.type = RecordingFile.TYPE.livestreaming
                    #     updateFile.save()
                        del existingFilesObj[file.get('id')]
                elif file.get('mimeType') == 'application/zip':
                    if file.get('id') not in existingGdriveIds:
                        createFile = self.unpack_zip(service, file, camera, user)
                        userFileList.append(createFile)
                    else:
                        del existingFilesObj[file.get('id')]
                
            if existingFilesObj:
                for key, value in existingFilesObj.items():
                    userDelFileList.append(value.id)
                    RecordingFile.objects.get(id=value.id).delete()

            users_files[user.phone_number] = {
                "createFileCount": len(userFileList),
                "deleteFileCount": len(userDelFileList)
            }

        for user in users:
            userData = users_files.get(user.phone_number)
            if userData:
              createFileCount = userData.get('createFileCount')
              deleteFileCount = userData.get('deleteFileCount')
              if (createFileCount and createFileCount > 0) or (deleteFileCount and deleteFileCount > 0):
                  send_whatsapp(f'{createFileCount} recording files successfully added and \
                                  {deleteFileCount} recording files successfully deleted', user.phone_number)
    
    def get_file_gdrive(self, service):
        query = f"(mimeType = 'video/mpeg' or mimeType = 'video/mp4' or mimeType = 'application/zip' or mimeType = 'image/jpeg') and trashed=false"
        filesFields = 'id, name, webViewLink, webContentLink, permissions, createdTime, modifiedTime, mimeType'
        response = service.files().list(
            q=query,
            fields=f"nextPageToken, files({filesFields})",
            ).execute()
        files = response.get('files')
        nextPageToken = response.get('nextPageToken')

        while nextPageToken:
            response = service.files().list(
                q=query,
                fields=f"nextPageToken, files({filesFields})",
                pageToken=nextPageToken
                ).execute()
            files.extend(response.get('files'))
            nextPageToken = response.get('nextPageToken')
        
        return files
    
    def unpack_zip(self, service: dict, file: dict, camera: dict, user: User):
        
        requestFile = service.files().get_media(fileId=file.get('id'))
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fd=fh, request=requestFile)
        
        done = False
        while not done:
            status, done = downloader.next_chunk()
        
        fh.seek(0)

        dirPath = f'{settings.MEDIA_ROOT}/file_camera/{camera.name}'
        isPathExist = os.path.exists(dirPath)
        if not isPathExist:
            os.makedirs(dirPath)

        with open(os.path.join(dirPath, file.get('name')), 'wb') as f:
            f.write(fh.read())
            f.close()
        
        # Extract all image from zip
        filePath = f"{dirPath}/{file.get('name')}"
        with zipfile.ZipFile(filePath, 'r') as zip_ref:
        
            extractDir = filePath.replace('.cma.zip', '')
            os.makedirs(extractDir, exist_ok=True)
            zip_ref.extractall(extractDir)
        
        # Setelah diekstrak, buat video dari gmbar
        videoName = extractDir.split('/')[-1] + '.mp4'
        videoPath = os.path.join(dirPath, videoName)

        os.remove(filePath) # Remove ZIP file  
        self.images_to_video(extractDir, videoPath) # Export as video
        shutil.rmtree(extractDir) # Remove ZIP directory
        videoPath = videoPath.replace(f'{settings.MEDIA_ROOT}/', '').replace("\\", '/')
        createFile = RecordingFile.objects.create(
            name=videoName,
            created_by=user,
            modified_by=user,
            type=RecordingFile.TYPE.googledrive,
            mimetype=RecordingFile.MIMETYPE.video,
            file=videoPath,
            camera=camera,
            google_drive_id=file.get('id'),
            is_from_gdrive=True
        )
        return createFile
    
    def images_to_video(self, extractDir: str, videoPath: str):
        if settings.ENV == 'LOCAL':
          valid_images = [i for i in os.listdir(extractDir) if i.endswith((".jpg", ".jpeg", ".png"))]

          first_image = cv2.imread(os.path.join(extractDir, valid_images[0]))
          h, w, _ = first_image.shape
          codec = cv2.VideoWriter_fourcc(*'avc1')
          vid_writer = cv2.VideoWriter(videoPath, codec, 30, (w, h))

          for img in valid_images:
              loaded_img = cv2.imread(os.path.join(extractDir, img))
              for _ in range(20):
                  vid_writer.write(loaded_img)

          vid_writer.release()
        elif settings.ENV == 'PRODUCTION':
          os.system(f"ffmpeg -y -framerate 1 -pattern_type glob -i '{extractDir}/*.jpg' -c:v libx264 -r 30 -pix_fmt yuv420p '{videoPath}'")
    
    def camera_object(self, file: dict, existingCamerasObj: dict, user: User):
        cameraName = file.get('name').split('_')
        camera = None
        if len(cameraName) > 2 :
            cameraName = f'{cameraName[0]}_{cameraName[1]}'

            # Create camera if not exist
            if not existingCamerasObj.get(cameraName):
                camera = Camera.objects.create(
                    name=cameraName,
                    ip_camera=cameraName[0],
                    created_by=user,
                    modified_by=user
                )
                existingCamerasObj[cameraName] = camera
            else:
                camera = existingCamerasObj.get(cameraName, None)
        return camera
