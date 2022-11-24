const forms = document.querySelectorAll('#follow-form')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value

// follow 기능
forms.forEach((form) => {
  form.addEventListener('submit', function(e) {
    e.preventDefault()
    const userId = e.target.dataset.userId

    axios({
      method: 'post',
      url: `/accounts/${userId}/follow/`,
      headers: {'X-CSRFToken' : csrftoken,},
    })
      .then((response) => {
        const isFollowed = response.data.is_followed
        const followBtn = document.querySelector(`#searchFollowBtn-${userId}`)
        if (isFollowed === true) {
          followBtn.classList.replace('search-follow-btn', 'search-unfollow-btn')
        } else {
          followBtn.classList.replace('search-unfollow-btn', 'search-follow-btn')
        }

        const followersCountTag = document.querySelector(`#search-followers-count-${userId}`)
        const followingsCountTag = document.querySelector(`#search-followings-count-${userId}`)
        const followersCount = response.data.followers_count
        const followingsCount = response.data.followings_count
        followersCountTag.innerText = followersCount
        followingsCountTag.innerText = followingsCount

      })
      .catch((error) => {
        console.log(error)
      })
  })
})