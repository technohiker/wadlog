

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

describe("Test the ability for a user to add a comment.", function() {
    let comment;
    let mockDatabase;
    let a;

    beforeAll(() => {
        comment = {
            'id': 4,
            'user_id': 3,
            'sender': 'test3',
            'target_user_id': '2',
            'receiver': 'test2',
            'time': 'Mon, 22 Aug 2022 21:28:43 GMT',
            'text': 'Jasmine testing rocks!',
            'pfp': '/static/images/default_profile.png'
        }
        a = 10;
    });
    xit('Should post comment info to the database.',function(){
        expect(a).toEqual(10);
    });
    it('Should use comment info to properly generate HTML.',function(){
        expect(htmlBuilder(comment).innerHTML).toContain('User: ');
    })
    xit('Test the whole flow of the event, from the user click to appending the comment.')
});