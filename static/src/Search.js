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

// indexMovies.addEventListener('click', (e) => {
//   e.preventDefault()
//   searchLists.forEach((element) => {
//     element.classList.add('hidden')
//   })
//   indexLists.forEach((element) => {
//     element.style.color = "#333333";
//   })
//   searchListMovies.classList.remove('hidden')
// })

// indexPeople.addEventListener('click', (e) => {
//   e.preventDefault()
//   searchLists.forEach((element) => {
//     element.classList.add('hidden')
//   })
//   indexLists.forEach((element) => {
//     element.style.color = "#333333";
//   })
//   searchListPeople.classList.remove('hidden')
// })

// indexGenre.addEventListener('click', (e) => {
//   e.preventDefault()
//   searchLists.forEach((element) => {
//     element.classList.add('hidden')
//   })
//   indexLists.forEach((element) => {
//     element.style.color = "#333333";
//   })
//   searchListGenre.classList.remove('hidden')
// })

// indexBooks.addEventListener('click', (e) => {
//   e.preventDefault()
//   searchLists.forEach((element) => {
//     element.classList.add('hidden')
//   })
//   indexLists.forEach((element) => {
//     element.style.color = "#333333";
//   })
//   searchListBooks.classList.remove('hidden')
// })