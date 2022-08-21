if(document.querySelector('#commentForm') == null){
    throw 'User not logged in, so comment submission form will not load.'
}

const userComments = document.querySelector('#userComments')
const commentForm = document.querySelector('#commentForm')
const commentText = document.querySelector('#commentText')
const userid = document.querySelector('div[userid]').getAttribute('userid')

commentForm.addEventListener('submit',e => {
    e.preventDefault()
    console.log(e.target)
    postComment(commentText.value)
})

async function postComment(text){
    data = {
        "comment": text,
        "target_user": userid
    }
    response = await axios.post('/api/comments/add',data)
    htmlBuilder(response.data)
}
function htmlBuilder(comment){
    console.log(comment)
    let hbTemplate = document.getElementById('commentTemplate').innerHTML
    let compiledHTML = Handlebars.compile(hbTemplate)
    let generatedHTML = compiledHTML(comment)

    console.log(generatedHTML)

    newComment = document.createElement('p')

    newComment.innerHTML = generatedHTML

    userComments.appendChild(newComment)

    commentText.value = ''
}