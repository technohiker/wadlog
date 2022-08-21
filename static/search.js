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

async function searchEvent(e){
    data = await showMods(e)
    modContainer.innerHTML = ''
    if(data.file.length == undefined){
        data = jsonFormat(data)
    }
    makeModObject(data)
    hideButtons()
}

async function showMods(e){

    let uri = 'https://www.doomworld.com/idgames/api/api.php'

    let query = f_query.value;
    let type = f_type.value;
    let sort = f_sort.value;
    let dir = f_dir.value;

    response = await axios.post('/search',{
        query: query,
        type: type,
        sort: sort,
        dir: dir
    })

    return response.data.content
}

function jsonFormat(json){
    //Create a list in order to work around API's structure limitations.
        //If one object is returned, you don't get a list, messing with loops.
        //Array is still named 'file' in order to match the Handlebar template's syntax.
        let file = []

        file.push(json.file)
        let object = { file }

        return object
}

async function makeModObject(json){

        //Experimenting with Handlebars.
        let hbTemplate = document.getElementById('htmlTemplate').innerHTML
        let compiledHTML = Handlebars.compile(hbTemplate)
        let generatedHTML = compiledHTML(json)

        modContainer.innerHTML = generatedHTML
}

function hideButtons(){

    buttons = document.querySelectorAll('.modButton')
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
    let modInfo = jsonBuilder(e.target.parentElement)
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

async function pullMod(json){
    response = await axios.post('/api/add_mod', json)

    return response.data
}

async function addMod(json){
//     -When button is clicked, check if mod is added to database.  If not, add it.
    result = await pullMod(json)

    response = await axios.post(`/api/add_record/${result.mod_id}`)

    return response.data
}

function jsonBuilder(obj){
    let values = obj.querySelectorAll('.valuePull')
    let json = {};
    for(i = 0; i < values.length; i++){
        child = values[i]
        json[child.getAttribute('json')] = child.getAttribute('val')
    }
    return json
}