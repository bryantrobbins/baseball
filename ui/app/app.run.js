/*@ngInject*/
function runWithBackend(){

}

/*@ngInject*/
function runMocked($httpBackend){

    var tableResponse = ['Pitching', 'Running', 'Stealing', 'Games', 'Players','Teams'];
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

    $httpBackend.whenGET(/.*\.tpl\.html/).passThrough();
    $httpBackend.whenGET(/.*\.svg/).passThrough();
    $httpBackend.whenGET(/.*\.css/).passThrough();

    $httpBackend.whenGET('/getDataSetNames').respond(tableResponse);
    $httpBackend.whenGET('/getDataSetMetadata').respond(metaResponse);
}

var run = {
    runWithBackend: runWithBackend,
    runMocked: runMocked
};

export default run;