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

async function clickEventListener(e){
    e.preventDefault()
    let result
    if(e.target.classList.contains('pullMod')){
        result = await pullMod(e.target.parentElement,e.target)
        if(result.status == "Success"){
            console.log("Success!");
            e.target.innerText = "Pulled!";
        }
        else if(result.status == "Already pulled."){
            e.target.innerText = "Already pulled.";
        }
    
        e.target.disabled = true
        e.target.classList.toggle('buttonPressed')
    }
    else if(e.target.classList.contains('addMod')){
        result = await addMod(e.target.parentElement)
    }
    console.log(result)

}

async function pullMod(modForm){
    json = await jsonBuilder(modForm)
    console.log(json)

    response = await axios.post('/api/add_mod', json)

    console.log(response.data.status)

    return response.data


    // -When button is clicked, make a call to the server to add all the mod info in.
    // -Organize mod object so you can properly pass the info in.
    // -Send Flask request with mod json data.
    //     -Make sure 'last_updated' is adjusted, if you're updating a new mod.
    // -Flash to show user that it was pulled.
}

async function addMod(modForm){
    console.log(modForm)
//     -When button is clicked, check if mod is added to database.  If not, add it.
    result = await pullMod(modForm)
    console.log(result)
//          -Return mod ID regardless.
//     -Make a call to the server to make a mod_record page.  Use aforementioned mod id.
    response = await axios.post(`/api/add_record/${result.mod_id}`)
    console.log(response)
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