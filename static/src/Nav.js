const navBar = document.getElementById('navbar')
const navSearchBtnDiv = document.getElementById('nav-search')
const navSearchBtnSpan = document.querySelector('#nav-search > span')
const navSearchBox = document.getElementById('nav-search-box')
const navSearchForm = document.getElementById('nav-search-form')
const navCenter = document.getElementById('navbar-center')
const navHomeDiv = document.getElementById('nav-home')
const navHomeSpan = document.querySelector('#nav-home > span')
const navLogo = document.getElementById('nav-logo')
const navTitle = document.getElementById('nav-title')
const navProfile = document.getElementById('nav-profile')
const profileModal = document.getElementById('profile-modal')
const navAroundDiv = document.getElementById('nav-around')
const navAroundSpan = document.querySelector('#nav-around > span')
// const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

const BASE_URL = 'http://127.0.0.1:8000'
const HOME_URL = '/books'
const ARROUND_URL = '/movies/recommended'

function btnClicked() {
  if(btnToggle.clicked == false) {
    navSearchBox.classList.remove('hidden')
    navCenter.classList.add('hidden')
    navSearchForm.value = '' 
    btnToggle.clicked = true
  }
  else {
    navSearchBox.classList.add('hidden')
    navCenter.classList.remove('hidden')
    btnToggle.clicked = false
  }
}

const btnToggle = { clicked: false }

navBar.addEventListener('click', (e) => {
  e.preventDefault()
  if(e.target === navSearchBtnDiv ||
    e.target === navSearchBtnSpan) {
    btnClicked()
  }
  else if(e.target === navSearchBox || 
    e.target === navSearchForm) {
  }
  else if(e.target === navHomeDiv ||
    e.target === navHomeSpan) {
    location.href = BASE_URL+HOME_URL
  }
  else if(e.target === navAroundDiv ||
    e.target === navAroundSpan) {
    location.href = BASE_URL+ARROUND_URL
  }
  else if(e.target === navLogo ||
    e.target === navTitle) {
    location.href = BASE_URL+HOME_URL
  }
  else if(e.target === navProfile) {
    profileClicked()
  }
  else if(btnToggle.clicked === true && modalToggle.clicked === true) {
    btnClicked()
    profileClicked()
  }
  else if(btnToggle.clicked === true) {
    btnClicked()
  }
  else if(modalToggle.clicked === true) {
    profileClicked()
  }
})

navSearchForm.addEventListener('search', (e) => {
  e.preventDefault()
})


const modalToggle = { clicked: false }

function profileClicked() {
  if(modalToggle.clicked == false) {
    profileModal.classList.remove('hidden')
    modalToggle.clicked = true
  }
  else {
    profileModal.classList.add('hidden')
    modalToggle.clicked = false
  }
}

const modalMyProfile = document.getElementById('profile-modal-myprofile')
const modalFriends = document.getElementById('profile-modal-friends')
const modalSettings = document.getElementById('profile-modal-settings')
const modalLogout = document.getElementById('profile-modal-logout')

const PROFILE_URL = ''
const FRIENDS_URL = ''
const SETTINGS_URL = ''
const LOGOUT_URL = '/accounts/logout/'

// modalMyProfile.addEventListener('click', (e) => {
//   e.preventDefault()
//   location.href = BASE_URL+PROFILE_URL
// })

// modalFriends.addEventListener('click', (e) => {
//   e.preventDefault()
//   location.href = BASE_URL+FRIENDS_URL
// })

// modalSettings.addEventListener('click', (e) => {
//   e.preventDefault()
//   location.href = BASE_URL+SETTINGS_URL
// })


// modalLogout.addEventListener('click', (e) => {
//   e.preventDefault()
//   console.log("clicked")
//   axios({
//     method: 'post',
//     url: `/accounts/logout`,
//     headers: {'X-CSRFToken' : csrftoken,},
//   })
//     .then((response) => {
//       console.log(response)
//     })
//     .catch((error) => {
//       console.log(error)
//     })
// })
  // location.href = BASE_URL+LOGOUT_URL
  // location.href = "{% url 'accounts:logout' %}"
