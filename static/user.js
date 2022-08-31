if(document.querySelector('#commentForm') == null){
    throw 'User not logged in, so comment submission form will not load.'
}

const userComments = document.querySelector('#userComments')
const commentForm = document.querySelector('#commentForm')
const commentText = document.querySelector('#commentText')
const userid = document.querySelector('div[userid]').getAttribute('userid')

commentForm.addEventListener('submit',e => {
    e.preventDefault()
    createComment(e.target.children[0].children[0]) //Send textarea object.
})

async function createComment(textArea){
    comment = await postComment(textArea, userid)
    if(comment.data.status == 'Unauthorized access.'){
        return
    }
    newComment = htmlBuilder(comment.data)
    userComments.appendChild(newComment)
    textArea.value = ''  //Remove user's comment after it is posted.
}

/** Send comment to database, then return data to use on client side. */
async function postComment(text, target_user){
    data = {
        "comment": text,
        "target_user_id": target_user
    }
    response = await axios.post('/api/comments/add',data)
    return response
}
/** Use Handlebars to generate a template so a posted comment shows up immediately. */
function htmlBuilder(comment){
    let hbTemplate = document.getElementById('commentTemplate').innerHTML
    let compiledHTML = Handlebars.compile(hbTemplate)
    let generatedHTML = compiledHTML(comment)

    let newComment = document.createElement('p')

    newComment.innerHTML = generatedHTML

    return newComment
}