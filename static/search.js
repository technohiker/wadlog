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
    obj = jsonFormat(data)
    makeModObject(obj)
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
        let list = []
        console.log(json)
        if(json.file.length > 1){
            for(obj of json.file){
                list.push(obj)
            }
        }
        else{
            list.push(json.file)
        }
        let object = { list }
        console.log(object)
        return object
}

async function makeModObject(json){


        //Experimenting with Handlebars.
        let hbTemplate = document.getElementById('htmlTemplate').innerHTML
        let compiledHTML = Handlebars.compile(hbTemplate)
        let generatedHTML = compiledHTML(json)

      //  console.log(generatedHTML)

        modContainer.innerHTML = generatedHTML
}

function hideButtons(){

    buttons = document.querySelectorAll('.modButton')
    for(i = 0; i < buttons.length; i++){
        if(!document.cookie.includes('user')){
            buttons[i].style.visibility = 'hidden'
        }
        else{
            buttons[i].addEventListener('click',clickEventListener)
        }
}
}

function clickEventListener(e){
    e.preventDefault()
    if(e.target.classList.contains('pullMod')){
        pullMod(e.target.parentElement,e.target)
    }
    else if(e.target.classList.contains('addMod')){
        addMod(e.target.parentElement)
    }
}

async function pullMod(modForm,button){
    json = await jsonBuilder(modForm)
    console.log(json)

    response = await axios.post('/api/add_mod', json)

    console.log(response.data.status)

    if(response.data.status == "Success"){
        button.innerText = "Pulled!"
        button.disabled = true
    }
    button.classList.toggle('buttonPressed')
    // -When button is clicked, make a call to the server to add all the mod info in.
    // -Organize mod object so you can properly pass the info in.
    // -Send Flask request with mod json data.
    //     -Make sure 'last_updated' is adjusted, if you're updating a new mod.
    // -Flash to show user that it was pulled.
}

async function addMod(modForm){
    console.log(modForm)
//     -When button is clicked, check if mod is in records.  If not, add it.
//     -Return mod ID regardless.
//  -Make a call to the server to make a mod_record page.  Use aforementioned mod id.

}

function jsonBuilder(obj){
    let json = {};
    for(i = 0; i < obj.children.length; i++){
        child = obj.children[i]
        if(!child.classList.contains('modButton'))
        json[child.id] = child.innerHTML
    }
    return json
}

/*

For both buttons, only add if user is logged in.
//Pull Mod Button:

                
                */

/*
//Add Mod Button:

 */

/* Mod call workflow:

- Make Axios call to get JSON from Idgames.
- Add this particular mod file to mod container below search.
- Need a function to convert the JSON into a mod object.
    - Should mod object contain all mod info, or just info to make another API call?

*/