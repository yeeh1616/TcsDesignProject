let util = require('./util');
exports.getProcess = function getProcess(arguments, rootPath, files){
    return {
        command: 'module_plus',
        args: ['tool', 'arguments', 'here'],
        options:{}
    };
};