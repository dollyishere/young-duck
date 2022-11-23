const store = document.getElementById('store')

const indexMovies = document.getElementById('search-index-movies')
const indexPeople = document.getElementById('search-index-people')
const indexGenre = document.getElementById('search-index-genre')
const indexBooks = document.getElementById('search-index-books')

const searchListMovies = document.getElementById('search-movies')
const searchListPeople = document.getElementById('search-people')
const searchListGenre = document.getElementById('search-genre')
const searchListBooks = document.getElementById('search-books')

const indexLists = [
  indexMovies,
  indexPeople,
  indexGenre,
  indexBooks,
]

const searchLists = [
  searchListMovies,
  searchListPeople,
  searchListGenre,
  searchListBooks,
]
indexLists.forEach(function(item, index) {
  item.addEventListener('click', function(e) {
    e.preventDefault()
    searchLists.forEach((element) => {
      element.classList.add('hidden')
    })
    indexLists.forEach((element) => {
      element.style.color = "#333333";
    })
    searchLists[index].classList.remove('hidden')
    indexLists[index].style.color = "#F5F5F5"
  })
})

function getStore() {
  try {
    return window.localStorage.getItem('isGenre')
  } catch(e) {
    window.localStorage.setItem('isGenre', 'false')
    return 'false'
  }
}

window.addEventListener('load', (e) => {
  e.preventDefault()
  const isGenre = getStore()
  if(isGenre === "true") {
    searchLists.forEach((element) => {
      element.classList.add('hidden')
    })
    indexLists.forEach((element) => {
      element.style.color = "#333333"
    })
    searchListGenre.classList.remove('hidden')
    indexGenre.style.color = "#F5F5F5"
    window.localStorage.removeItem('isGenre')
    window.localStorage.setItem('isGenre', 'false')
  }
})