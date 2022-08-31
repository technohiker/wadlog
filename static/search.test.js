

/*
it('test functionName().  Insert description about the goal of this test., function() {
    //Write data for test.
        //let a = 10
        //let b = 20
    
    //Write tests.
        //expect(functionName(a,b)).toEqual(-10);
        //expect(functionName(b,a)).toEqual(10);
    
})

beforeEach() {
    //Function used to run code before each test is ran.
    //afterEach function exists as well.
    //There is also beforeAll and afterAll.
}
*/

/*

How do we add HTML data?

*/

describe("Test JS code for fetching mod information from Idgames.", () =>{
    beforeAll(() => {
        singleMod = {
            "content":{
                "file":{
                    "id":11944,
                    "title":"Scythe",
                    "dir":"levels/doom2/megawads/",
                    "filename":"scythe.zip",
                    "size":2086863,
                    "age":1049950800,
                    "date":"2003-04-10",
                    "author":"Erik Alm, with guest mapper Kim \"Torn\" Bach",
                    "email":"erik_a80@hotmail.com",
                    "description":"A 32 level megawad for doom2. This megawad doesn't have perfect texture alignment, insane detail and fantasticly hard gameplay. Instead it focuses on small fun maps to blast through without much thought about defense. The difficulty rises steadily as you go through the maps and the last few should challenge even the best.",
                    "rating":4.1225,
                    "votes":408,
                    "url":"https://www.doomworld.com/idgames/levels/doom2/megawads/scythe",
                    "idgamesurl":"idgames://levels/doom2/megawads/scythe.zip"
                    }
                }
        }
        doubleMod = {
            "content":{
            "file":[{
                "id":11944,
                "title":"Scythe",
                "dir":"levels/doom2/megawads/",
                "filename":"scythe.zip",
                "size":2086863,
                "age":1049950800,
                "date":"2003-04-10",
                "author":"Erik Alm, with guest mapper Kim \"Torn\" Bach",
                "email":"erik_a80@hotmail.com",
                "description":"A 32 level megawad for doom2. This megawad doesn't have perfect texture alignment, insane detail and fantasticly hard gameplay. Instead it focuses on small fun maps to blast through without much thought about defense. The difficulty rises steadily as you go through the maps and the last few should challenge even the best.",
                "rating":4.1225,
                "votes":408,
                "url":"https://www.doomworld.com/idgames/levels/doom2/megawads/scythe",
                "idgamesurl":"idgames://levels/doom2/megawads/scythe.zip"
                },
                {
                "id":11944,
                "title":"Scythe",
                "dir":"levels/doom2/megawads/",
                "filename":"scythe.zip",
                "size":2086863,
                "age":1049950800,
                "date":"2003-04-10",
                "author":"Erik Alm, with guest mapper Kim \"Torn\" Bach",
                "email":"erik_a80@hotmail.com",
                "description":"A 32 level megawad for doom2. This megawad doesn't have perfect texture alignment, insane detail and fantasticly hard gameplay. Instead it focuses on small fun maps to blast through without much thought about defense. The difficulty rises steadily as you go through the maps and the last few should challenge even the best.",
                "rating":4.1225,
                "votes":408,
                "url":"https://www.doomworld.com/idgames/levels/doom2/megawads/scythe",
                "idgamesurl":"idgames://levels/doom2/megawads/scythe.zip"
                }]
            }
        }
    })

    it("Receive info from Idgames website. showMods()",() => {
        //showMods()
        let spySuccess = jasmine.createSpy('sendMod')
        let apiResource = 'https://www.doomworld.com/idgames/api/api.php?action=search&query=scythe&type=title'
        jasmine.Ajax.withMock(function() {
            //Create mock Request object, and have spy check response.
            testRequest = new XMLHttpRequest();
            testRequest.onreadystatechange = function(a){
                if(this.readyState == this.DONE){
                    expect(this.status).toEqual(200)
                    spySuccess(this.response)
                }
            }

            testRequest.open('POST',apiResource)
            testRequest.send();

            expect(jasmine.Ajax.requests.mostRecent().url).toEqual(apiResource)
            expect(spySuccess).not.toHaveBeenCalled()
    
            //Call mock API.
            jasmine.Ajax.requests.mostRecent().respondWith({
                "status": 200,
                "response": singleMod
            })

            //Check on spy.
            expect(spySuccess).toHaveBeenCalled()
            expect(spySuccess).toHaveBeenCalledWith(singleMod)
            expect(spySuccess).toHaveBeenCalledTimes(1)
        })
    })
    it("Convert info from Idgames into a json object with length, for proper iteration.  jsonFormat()",() => {
        data = jsonFormat(singleMod.content)
        expect(data.file.length).toBeDefined()
    })
    it("Create an HTML object out of the searched mod. makeModObject()",() => {
        data1 = jsonFormat(singleMod.content)
        expect(makeModObject(data1)).toContain('hiddenValue')
        data2 = jsonFormat(doubleMod.content)
        expect(makeModObject(data2)).toContain('hiddenValue')
    })
    it("Hide all the buttons of the mod objects. hideButtons()",() => {
        div = document.createElement('div')
        html = makeModObject(doubleMod.content)
        div.innerHTML = html

        document.cookie = 'user=Test User'
            hideButtons(div)
            expect(div.innerHTML).not.toContain('none')
        document.cookie = 'user=; expires=Sat, 01 Jan 2022 00:00:00 GMT;'
            hideButtons(div)
            expect(div.innerHTML).toContain('none')

    })
});

describe("Add mod info to Mods or Records tables.",()=>{
    beforeAll(() => {
        searchedMod = document.createElement('div')
        searchedMod.innerHTML = 
            `<form name="formMod" id="formMod-38217" class="searchedMod card" method="POST">
                    <p class="hiddenValue valuePull" id="search-id" json="id" val="38217">38217</p>
                    <p class="hiddenValue valuePull" id="search-url" json="url" val="http://www.testurl.com">http://www.testurl.com</p>
                    <p class="hiddenValue valuePull" id="search-dir" json="dir" val="this/directory/is/fake">this/directory/is/fake</p>
                    <div class="card-header">
                        <h2><a href="http://www.testurl.com" id="search-title"  json="title" val="Test Game" class="title valuePull">Test Game</a></h2>
                    </div>
                    <div class="card-body d-flex flex-row">
                        <ul class="d-flex flex-column flex-wrap col-sm-3 noBullets">
                            <li class="valuePull" json="author" val="Tom Hall"><b>Author:</b>Tom Hall</li>
                            <li class="valuePull" json="date" val="2003-01-02"><b>Release Date:</b>2003-01-03</li>
                                <li class="valuePull" id="search-rating" json="rating" val="4.53"><b>Score:</b> 4.53 of 5</li>
                                <li class="valuePull" id="search-votes" json="votes" val="100">100 ratings</li>
                        </ul>
                        <div class="col-sm-9">
                            <h3>Description:</h3>
                            <article class="valuePull" json="description" val="Test Description">Test Description</article>
                        </div>
                    </div>

                <button class="modButton pullMod btn btn-primary">Pull Mod</button>
                <button class="modButton addMod btn btn-primary">Add Mod</button>
                
            </form>`
        modResponse = {
            'id': 4,
            'user_id': 3,
            'sender': 'test3',
            'target_user_id': '2',
            'receiver': 'test2',
            'time': 'Mon, 22 Aug 2022 21:28:43 GMT',
            'text': 'This is a test comment.',
            'pfp': '/static/images/default_profile.png'
        }
        recordResponse = {
            'status': 'Added!',
            'record_id': 5
        }
    })
    it("Sending info to Mods/Records tables respectively. addMod()",() => {
        //Modified from https://jasmine.github.io/tutorials/mocking_ajax.

        let spySuccess = jasmine.createSpy('sendMod')
        let apiResource1 = 'api/add_mod'
        let apiResource2 = 'api/add_record/1'
        jasmine.Ajax.withMock(function() {
            //Create mock Request object, and have spy check response.
            testRequest = new XMLHttpRequest();
            testRequest.onreadystatechange = function(a){
                if(this.readyState == this.DONE){
                    expect(this.status).toEqual(200)
                    spySuccess(this.response)
                }
            }

            testRequest.open('POST',apiResource1)
            testRequest.send();

            expect(jasmine.Ajax.requests.mostRecent().url).toEqual(apiResource1)
            expect(spySuccess).not.toHaveBeenCalled()
    
            //Call mock API.
            jasmine.Ajax.requests.mostRecent().respondWith({
                "status": 200,
                "response": modResponse
            })

            //Check on spy.
            expect(spySuccess).toHaveBeenCalled()
            expect(spySuccess).toHaveBeenCalledWith(modResponse)
            expect(spySuccess).toHaveBeenCalledTimes(1)

            //Set up second call.
            testRequest.open('POST',apiResource2)
            testRequest.send();

            expect(jasmine.Ajax.requests.mostRecent().url).toEqual(apiResource2)
            
            //Make second call.
            jasmine.Ajax.requests.mostRecent().respondWith({
                "status": 200,
                "response": recordResponse
            })
            
            //Spy should've been called twice.
            expect(spySuccess).toHaveBeenCalled()
            expect(spySuccess).toHaveBeenCalledWith(recordResponse)
            expect(spySuccess).toHaveBeenCalledTimes(2)

        })
})
    it("Turn pulled mod info in HTML into a JSON object. jsonBuilder()",() => {
        result = jsonBuilder(searchedMod.firstChild)
        expect(result['id']).toEqual('38217')
    })
});