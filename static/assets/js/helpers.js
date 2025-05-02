function onlyNumber(tag){
    tag.value = tag.value.replace(/[^0-9]/, '');
}

function onlyAlpha(tag){
    tag.value = tag.value.replace(/[^a-z\s]/gi, '');
}

// Function Format Date Time
function dateTimeFormat(date) {
    var newdate = new Date(date)
    var dd = String(newdate.getDate()).padStart(2, '0');
    var mm = String(newdate.getMonth() + 1).padStart(2, '0'); //January is 0!
    var yyyy = newdate.getFullYear();
    var time = newdate.toLocaleTimeString("en-ID")

    return `${dd}-${mm}-${yyyy} ${time}`;
}

// Function Format Date
function formatDate(date) {
    var d = new Date(date),
        month = '' + (d.getMonth() + 1),
        day = '' + d.getDate(),
        year = d.getFullYear();

    if (month.length < 2) 
        month = '0' + month;
    if (day.length < 2) 
        day = '0' + day;

    return [year, month, day].join('-');
}

// Clean Params
function cleanParams(params) {
    params.forEach((param, i) => {
        if (param === '') params.delete(i)
    })
    return params
}

function reformatText(value) {
    return titleCase(value.replace("-", " "))
}

function titleCase(str) {
    if(str != null){
        return str.toLowerCase().replace(/(^|\s)(\w)/g, function(x) {
            return x.toUpperCase();
        });
    }else{
        return null
    }
}
