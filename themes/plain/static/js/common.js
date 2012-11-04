localize_time = function(status_date) {
    var d = new Date(Date.UTC(status_date))
    d.setTime(status_date*1000)
    d.setTimezone()
    var local_day = d.toLocaleDateString()
    var local_time = d.toLocaleTimeString()
    var times = local_time.split(":")
    var ampm = "AM"
    if (times[0] > 12) {
        times[0] = times[0] - 12;
        ampm = "PM"
    }
    return times.join(":") + " " + ampm + " " + local_day;
};