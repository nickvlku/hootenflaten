localize_time = function(status_date) {
    d = new Date(0)
    d.setUTCSeconds(status_date*1000)
    local_time = d.toString('hh:mm:ss tt dddd, MMMM dd, yyyy');
    if (local_time.indexOf("00:") == 0) {
        s = local_time.split(":")
        s[0] = "12"
        local_time = s.join(":")
    }
    return local_time;
};

