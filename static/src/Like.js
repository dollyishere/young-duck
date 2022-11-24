const form = document.getElementById('like-forms')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

form.addEventListener('submit', function(event) {
  event.preventDefault()
  const bookId = event.target.dataset.bookId

  axios({
    method: 'post',
    url: `/books/${bookId}/like/`,
    headers: {'X-CSRFToken': csrftoken},
  })
    .then((response) => {
      const isLiked = response.data.is_liked
      const likeBtn = document.getElementById(`like-${bookId}`)

      if(isLiked == true) {
        likeBtn.classList.replace("like-btn", "unlike-btn")
      } else {
        likeBtn.classList.replace("unlike-btn", "like-btn")
      }

      const likeCountTag = document.getElementById('like-cnt')
      const likeCount = response.data.like_count
      likeCountTag.innerText = likeCount
    })
    .catch((error) => {
      console.log(error.response)
    })
})