describe("Test the ability for a user to add a comment.", function() {
    let testResponse;

    beforeAll(() => {
        testResponse = {
            'id': 4,
            'user_id': 3,
            'sender': 'test3',
            'target_user_id': '2',
            'receiver': 'test2',
            'time': 'Mon, 22 Aug 2022 21:28:43 GMT',
            'text': 'This is a test comment.',
            'pfp': '/static/images/default_profile.png'
        }
    });
    it('Test calling the API.',function(){

        //Modified from https://jasmine.github.io/tutorials/mocking_ajax.

        spySuccess = jasmine.createSpy('postComment')
        apiResource = 'api/comments/add'
        jasmine.Ajax.withMock(function() {
            testRequest = new XMLHttpRequest();
            testRequest.open('POST',apiResource)
            testRequest.send();
            testRequest.onreadystatechange = function(a){
                if(this.readyState == this.DONE){
                    expect(this.status).toEqual(200)
                    spySuccess(this.response)
                }
            }
            expect(jasmine.Ajax.requests.mostRecent().url).toEqual(apiResource)
            expect(spySuccess).not.toHaveBeenCalled()
    
            jasmine.Ajax.requests.mostRecent().respondWith({
                "status": 200,
                "response": testResponse
            })
            
            expect(spySuccess).toHaveBeenCalled()
            expect(spySuccess).toHaveBeenCalledWith(testResponse)
            expect(spySuccess).toHaveBeenCalledTimes(1)
        })
    });
    it('Should use comment info to properly generate HTML. htmlBuilder()',function(){
        data = htmlBuilder(testResponse)
        expect(htmlBuilder(testResponse).innerHTML).toContain('User: ');
        expect(htmlBuilder(testResponse).innerHTML).toContain('</div>');
        expect(htmlBuilder(testResponse).innerHTML).toContain('Mon, 22 Aug 2022 21:28:43 GMT');
    })
});