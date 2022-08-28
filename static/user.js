if(document.querySelector('#commentForm') == null){
    throw 'User not logged in, so comment submission form will not load.'
}

const userComments = document.querySelector('#userComments')
const commentForm = document.querySelector('#commentForm')
const commentText = document.querySelector('#commentText')
const userid = document.querySelector('div[userid]').getAttribute('userid')

commentForm.addEventListener('submit',e => {
    e.preventDefault()
    createComment(e)
})

async function createComment(e){
    comment = await postComment(commentText.value)
    if(comment.data.status == 'Unauthorized access.'){
        return
    }
    newComment = htmlBuilder(comment.data)
    userComments.appendChild(newComment)
    commentText.value = ''  //Remove user's comment after it is posted.
}

/** Send comment to database, then return data to use on client side. */
async function postComment(text){
    data = {
        "comment": text,
        "target_user_id": userid
    }
    response = await axios.post('/api/comments/add',data)
    return response
}
/** Use Handlebars to generate a template so a posted comment shows up immediately. */
function htmlBuilder(comment){
    console.log(comment)
    let hbTemplate = document.getElementById('commentTemplate').innerHTML
    let compiledHTML = Handlebars.compile(hbTemplate)
    let generatedHTML = compiledHTML(comment)

    let newComment = document.createElement('p')

    newComment.innerHTML = generatedHTML
    console.log(newComment)

    return newComment
}