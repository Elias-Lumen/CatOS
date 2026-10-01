// Keep CatOS synced with the date and timezone
// reported by the user's device.
//
// The database stores timestamps in UTC.
// Pages that depend on "today" can use these
// cookies to interpret dates in the user's timezone.

function updateDeviceTimeCookies() {

    const now = new Date();

    const localDate = [
        now.getFullYear(),
        String(
            now.getMonth() + 1
        ).padStart(
            2,
            "0"
        ),
        String(
            now.getDate()
        ).padStart(
            2,
            "0"
        )
    ].join("-");

    document.cookie =
        `catos_local_date=${localDate}; path=/; SameSite=Lax`;

    document.cookie =
        `catos_timezone_offset=${now.getTimezoneOffset()}; path=/; SameSite=Lax`;
}


// Update immediately whenever a CatOS page loads.
updateDeviceTimeCookies();