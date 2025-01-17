const date = new Date()
const hour = date.getHours() +":"+ date.getMinutes()

const openTimes = document.getElementsByClassName('open_time')
const closeTimes = document.getElementsByClassName('close_time')
const isOpenElements = document.getElementsByClassName('is_open')

function convertToMinutes(time) {
    const [hours, minutes] = time.split(':').map(Number);
    return hours * 60 + minutes;
}

for (let i=0 ; i<isOpenElements.length ; i++) {
    const currentHour = convertToMinutes(hour)
    const openTime = convertToMinutes(openTimes[i].textContent)
    const closeTime = convertToMinutes(closeTimes[i].textContent)

    if (currentHour >= openTime && currentHour <= closeTime) {
        isOpenElements[i].innerHTML = "<span class='badge bg-success'>Buka</span>"
    } else {
        isOpenElements[i].innerHTML = "<span class='badge bg-danger'>Tutup</span>"
    }
}

// filter form
const params = new URLSearchParams(location.search)

const selectCategoryForm = document.getElementById('select-category-form')
const searchInput = document.getElementById('searchInput')

if (params.get('category')) {
    selectCategoryForm.value = params.get('category')
}

if (params.get('s')) {
    searchInput.value = params.get('s')
}

const filter = () => {
    let url = '/search?s='+searchInput.value+'&category='+selectCategoryForm.value
    if (searchInput.value == '' && selectCategoryForm.value == '') {
        url = '/'
    }
    location.href = url
}