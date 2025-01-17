const notificationList = document.getElementById('notification')
const userId = document.getElementById('user_id')
const notifIcon = document.getElementById('notif_icon')

const url = 'http://localhost:5000/api/notifications/'
const optionsDateFormat = {
  weekday: 'long',
  year: 'numeric',
  month: 'long',
  day: 'numeric',
}

const getNotifications = async (userId) => {
    let totalNotif = 0

    const resp = await fetch(url+`${userId}`)
    const data = await resp.json()

    if (data['data'].length > 0) {
        notificationList.innerHTML = '<h5 class="dropdown-item disabled">Notifikasi</h5>'
        for(let i=0 ; i<data['data'].length ; i++) {

                if (data['data'][i].is_read === false) {
                    notificationList.innerHTML += `
                        <div class="dropdown-item text-wrap" style="background-color: #FEFF9F" onclick="notCloseDropdown(event)">
                            <li style='font-size: 12px'>
                                <strong>${data['data'][i].title}</strong><br><small class='fw-semibold'>${new Date(data['data'][i].created_at).toLocaleDateString('id',optionsDateFormat)}</small><br>${data['data'][i].message}<br>
                                <small class="text-primary" style="cursor: pointer" tabindex="-1" onclick="signAsRead(event, ${data['data'][i].id}); return false;">Tandai sudah baca</small>
                            </li>
                        </div><li><hr class="m-0 dropdown-divider"></li>
                    `
                    totalNotif++
                } else {
                    notificationList.innerHTML += `
                        <div class="dropdown-item text-wrap bg-light" onclick="notCloseDropdown(event)">
                            <li style='font-size: 12px'><strong>${data['data'][i].title}</strong><br><small class='fw-semibold'>${new Date(data['data'][i].created_at).toLocaleDateString('id',optionsDateFormat)}</small><br>${data['data'][i].message}</li>
                        </div><li><hr class="m-0 dropdown-divider"></li>`
                }
        }
    }

    if (totalNotif > 0) {
        notifIcon.innerHTML = `<sup><span class="badge bg-warning">${totalNotif}</span></sup>`
    } else {
        notifIcon.innerHTML = ''
    }
}

getNotifications(userId.value)

const signAsRead = async (event, notificationId) => {
    event.stopPropagation();
    const resp = await fetch(`${url}${notificationId}/set-status-read`)
    if (resp.ok) {
        getNotifications(userId.value)
    }
}

const notCloseDropdown = (event) => {
    event.stopPropagation();
}