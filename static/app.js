const searchForm = document.querySelector('#formSearch')
const modContainer = document.querySelector('#modContainer')

const f_query = document.querySelector('#query')
const f_type = document.querySelector('#type')
const f_sort = document.querySelector('#sort')
const f_dir = document.querySelector('#dir')

searchForm.addEventListener('submit', function(e){
    e.preventDefault()
    pullMod(e)
})

async function pullMod(e){

    let uri = 'https://www.doomworld.com/idgames/api/api.php'

    let query = f_query.value;
    let type = f_type.value;
    let sort = f_sort.value;
    let dir = f_dir.value;

    console.log(`${uri}?action=search
    &query=${query}&type=${type}&sort=${sort}&dir=${dir}`)
/*
    response = axios.get(`${uri}?action=search
        &query=${query}&type=${type}&sort=${sort}&dir=${dir}`)
*/

    response = await axios.post('/search',{
        query: query,
        type: type,
        sort: sort,
        dir: dir
    })
    console.log(response.data)
}


/* Mod call workflow:

- Will WTForms go off even with e.PreventDefault?

- Make Axios call to get JSON from Idgames.
- Add this particular mod file to mod container below search.
- Need a function to convert the JSON into a mod object.
    - Should mod object contain all mod info, or just info to make another API call?

*/