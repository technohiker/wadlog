const searchForm = document.querySelector('#formSearch')
const modContainer = document.querySelector('#modContainer')

const f_query = document.querySelector('#query')
const f_type = document.querySelector('#type')
const f_sort = document.querySelector('#sort')
const f_dir = document.querySelector('#dir')

searchForm.addEventListener('submit', function(e){
    e.preventDefault()
    searchEvent(e)
})

/** Called upon submitting Search form.
 *  Pulls info from Idgames API, then converts it into HTML.
 */
async function searchEvent(e){
    json = {
        "query": f_query.value,
        "type": f_type.value,
        "sort": f_sort.value,
        "dir": f_dir.value
    }
    data = await showMods(json)

    modContainer.innerHTML = ''

    try{
        if(data.file.length == undefined){
            data = jsonFormat(data)
        }
    
        cleanData = removeBRTags(data)
    
        htmlMod = makeModObject(cleanData)
    
        modContainer.innerHTML = htmlMod
        hideButtons(modContainer)
    }
    catch(error){
        modContainer.innerHTML = 'No file found.  Please check if you typed your search in correctly.'
    }
}

/** Use search form info to pull info from Idgames API. 
 * Calls Flask instead of Idgames directly to get around CSRF.
*/
async function showMods(data){
    response = await axios.post('/search',data)
    return response.data.content
}
/** Removes any <br> tags in strings and replaces them with proper line breaks. */
function removeBRTags(json){
    console.log(json)
    for(file of json.file){
        file['description'] = file['description'].replaceAll( "<br>",'\n')
    }
    return json
}

/** Build Idgames response into a proper JSON object.
 *  Designed to work regardless of whether you get one or many objects.
 */
function jsonFormat(json){
    //Array is still named 'file' in order to match the Handlebar template's syntax.
    let file = []

    file.push(json.file)
    let object = { file }

    return object
}

/** Convert JSON into HTML object with Handlebars. */
function makeModObject(json){

        let hbTemplate = document.getElementById('htmlTemplate').innerHTML
        let compiledHTML = Handlebars.compile(hbTemplate)
        let generatedHTML = compiledHTML(json)

        return generatedHTML
}

/** Hide form buttons.  Called when user is not logged in. */
function hideButtons(html){

    buttons = html.querySelectorAll('.modButton')
    for(i = 0; i < buttons.length; i++){
        if(!document.cookie.includes('user')){
            buttons[i].style.display = 'none'
        }
        else{
            buttons[i].addEventListener('click',clickEventListener)
        }
}
}

async function clickEventListener(e){
    e.preventDefault()
    let modInfo = jsonBuilder(e.target.parentElement.parentElement)
    let result
    if(e.target.classList.contains('pullMod')){
        result = await pullMod(modInfo)
    }
    else if(e.target.classList.contains('addMod')){
        result = await addMod(modInfo)
    }
    e.target.innerText = result.status
    e.target.disabled = true
}

/** Send HTML info of mod record to database.*/
async function pullMod(json){
    response = await axios.post('/api/add_mod', json)

    return response.data
}

/** Add a mod recorded in the database to Records table.
 * If mod doesn't exist, add it.
 */
async function addMod(json){
    result = await pullMod(json)

    response = await axios.post(`/api/add_record/${result.mod_id}`)

    return response.data
}

/** Take specific values from HTML object and create a JSON object out of them. */
function jsonBuilder(obj){
    let values = obj.querySelectorAll('.valuePull')
    let json = {};
    for(i = 0; i < values.length; i++){
        child = values[i]
        json[child.getAttribute('json')] = child.getAttribute('val')
    }
    return json
}