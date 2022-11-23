const genreTags = document.querySelectorAll('.card-genre-style')
const SEARCH_BASE_URL = 'http://127.0.0.1:8000/movies/search/?nav-search-form='

function movePage (genre) {
  location.href = SEARCH_BASE_URL + genre
}

function setStore (genre) {
  window.localStorage.setItem('isGenre', 'true')
  return movePage(genre)
}

function removeStore (genre) {
  window.localStorage.removeItem('isGenre')
  return setStore(genre)
}

genreTags.forEach((element) => {
  element.addEventListener('click', (e) => {
    const genre = e.target.innerText
    removeStore(genre)
  })
})