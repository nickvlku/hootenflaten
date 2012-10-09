localize_time = function(status_date) {
    local_time = new Date(status_date*1000).toString('hh:mm:ss tt dddd, MMMM dd, yyyy');
    if (local_time.indexOf("00:") == 0) {
        s = local_time.split(":")
        s[0] = "12"
        local_time = s.join(":")
    }
    return local_time;
};

