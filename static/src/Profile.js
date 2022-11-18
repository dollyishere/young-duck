const form = document.querySelector('#follow-form')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

// follow 기능
form.addEventListener('submit', function (event) {
  event.preventDefault()

  const userId = event.target.dataset.userId

  axios({
    method: 'post',
    url: `/accounts/${userId}/follow/`,
    headers: {'X-CSRFToken' : csrftoken,},
  })
    .then((response) => {
      const isFollowed = response.data.is_followed
      const followBtn = document.querySelector('#followBtn')
      if (isFollowed === true) {
        followBtn.innerText = '언팔로우'
      } else {
        followBtn.innerText = '팔로우'
      }

      const followersCountTag = document.querySelector('#followers-count')
      const followingsCountTag = document.querySelector('#followings-count')
      const followersCount = response.data.followers_count
      const followingsCount = response.data.followings_count
      followersCountTag.innerText = followersCount
      followingsCountTag.innerText = followingsCount

    })
    .catch((error) => {
      console.log(error)
    })
})

// profile edit 기능