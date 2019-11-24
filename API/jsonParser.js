
//Obtains the current task
var getCurrentTask = function(jsonFile){

    //Terminating conditions.
    if(jsonFile === undefined){
        return(undefined);
    }

    let remainingNode;

    //If we are currently in an array, check each node.
    if(jsonFile.length !== undefined){
        for(let i = 0; i < jsonFile.length; i++){
            if(jsonFile[i].tag === "none"){
                return(undefined); //We reached end.
            }
            if(jsonFile[i].response === "none"){
                return(jsonFile[i]);
            }
        }
        //We are at end of this array. Check if this node goes deeper.
        remainingNode = jsonFile[jsonFile.length-1];
    } else {
        remainingNode = jsonFile;
        if(remainingNode.tag === "none"){
            return(undefined);
        }
        if(remainingNode.response === "none"){
            return(remainingNode);
        }
    }

    //Check if response is a elif
    if(remainingNode.tag === "elif" && remainingNode.response === "true"){
        return(getCurrentTask(remainingNode.true));
    } else if (remainingNode.tag === "elif" && remainingNode.response === "false"){
        return(getCurrentTask(remainingNode.false));
    }

    //Neither meaning that response was an error and we conclude.
    return(undefined);

}


//Updates the current task.
var updateCurrenttask = function(update){
    
}


module.exports = {
    getCurrentTask:getCurrentTask
}