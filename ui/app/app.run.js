/*@ngInject*/
function runWithBackend(){

}

/*@ngInject*/
function runMocked($httpBackend){

    var tableResponse = [{"name":"Lahman: Batting (Career)","id":"lahman-batting-career"},{"name":"Lahman: Batting (Player/Team)","id":"lahman-batting-player-team"},{"name":"Lahman: Batting (Player/Year)","id":"lahman-batting-player-year"},{"name":"Lahman: Batting (Team/Year)","id":"lahman-batting-team-year"},{"name":"Lahman: Pitching (Career)","id":"lahman-pitching-career"},{"name":"Lahman: Pitching (Player/Team)","id":"lahman-pitching-player-team"},{"name":"Lahman: Pitching (Player/Year)","id":"lahman-pitching-player-year"},{"name":"Lahman: Pitching (Team/Year)","id":"lahman-pitching-team-year"}];
    var metaResponse = {
        rowDesc: "Each row is a Player Stint - a set of games that a single player participated in for a single team in a single season. A player may have multiple stints within a single season, and each will have a unique value in the 'stint' column.",
        colMetaData:[
            {colName:'playerID', colType:'String', colDesc:'The ID'},
            {colName:'yearID', colType:'Number', colDesc:'The Year'},
            {colName:'stint', colType:'Number', colDesc:'ID for this sequence of games (unique to player and year)'},
            {colName:'teamID', colType:'String', colDesc:'The team of the player'},
            {colName:'lgID', colType:'String', colDesc:'League ID'},
            {colName:'G',colType:'Count',colDesc:'Games'},
            {colName:'AB', colType:'Count', colDesc:'At Bats'},
            {colName:'R', colType:'Count', colDesc:'Runs'},
            {colName:'H', colType:'Count', colDesc:'Hits'},
            {colName:'2B', colType:'Count', colDesc:'Doubles'},
            {colName:'3B', colType:'Count', colDesc:'Triples'},
            {colName:'HR', colType:'Count', colDesc:'Home Runs'},
            {colName:'RBI', colType:'Count', colDesc:'Runs Batted In'},
            {colName:'SB', colType:'Count', colDesc:'Stolen Bases'},
            {colName:'CS', colType:'Count', colDesc:'Caught Stealing'},
            {colName:'BB', colType:'Count', colDesc:'Walks (Base on Balls)'},
            {colName:'SO', colType:'Count', colDesc:'Strikeouts'},
            {colName:'IBB',colType:'Count', colDesc:'Intentional Walks'},
            {colName:'HBP',colType:'Count', colDesc:'Hit By Pitch'},
            {colName:'SH',colType:'Count', colDesc:'Sacrifice Hits'},
            {colName:'SF',colType:'Count', colDesc:'Sacrifice Flies'},
            {colName:'GIDP', colType:'Count', colDesc:'Grounded Into Double Play'}]};
    var exportResponse = [{
        name: 'table',
        fields: [
            {
                name: 'orderBy',
                desc: 'Order By',
                values:'selected'
            },
            {
                name:'direction',
                desc:'Direction',
                values:[
                    {id:'desc', name: 'Descending'},
                    {id:'asc', name:'Ascending'}
                ]
            }
        ]
    }];

    $httpBackend.whenGET(/.*\.tpl\.html/).passThrough();
    $httpBackend.whenGET(/.*\.svg/).passThrough();
    $httpBackend.whenGET(/.*\.css/).passThrough();

    $httpBackend.whenGET(/api\/getTables/).respond(tableResponse);
    $httpBackend.whenGET(/api\/getMetadata\/.+/).respond(metaResponse);
    $httpBackend.whenGET('/api/getExportData').respond(exportResponse);

    $httpBackend.whenPOST('/api/submitJob').respond("http://imgur.com");
}

var run = {
    runWithBackend: runWithBackend,
    runMocked: runMocked
};

export default run;