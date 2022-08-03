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
    makeModObject(data)
}

async function logout(e){
    response = await axios.get('/logout')
    if(response.data.logout == 'Success'){
        localStorage.removeItem('userID')
        document.location.href = '/search'
    }

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

async function makeModObject(json){
    console.log(json)
        //Experimenting with Handlebars.
        let hbTemplate = document.getElementById('htmlTemplate').innerHTML
        let compiledHTML = Handlebars.compile(hbTemplate)
        let generatedHTML = compiledHTML(json)

     //   console.log(generatedHTML)

        modContainer.innerHTML = generatedHTML

        response = await axios.get('/api/login_status')
        buttons = document.querySelectorAll('.modButton')
        if(response.data.status == 'False'){
            for(i = 0; i < buttons.length; i++){
                buttons[i].style.visibility = 'hidden'
            }
        }

}

function pullMod(){
    // -When button is clicked, make a call to the server to add all the mod info in.
    // -Organize mod object so you can properly pass the info in.
    // -Send Flask request with mod json data.
    //     -Make sure 'last_updated' is adjusted, if you're updating a new mod.
    // -Flash to show user that it was pulled.
}

function addMod(){
//     -When button is clicked, check if mod is in records.  If not, add it.
//     -Return mod ID regardless.
//  -Make a call to the server to make a mod_record page.  Use aforementioned mod id.

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