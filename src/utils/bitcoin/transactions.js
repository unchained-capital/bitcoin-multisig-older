const BigNumber = require('bignumber.js');

var { estimateTransactionFees } = require('./btc_utils');


function finalizeOutputs(remainingAddress, utxos, fixedOutputs, fees) {

    let numOutputs = Object.keys(fixedOutputs).length + 1;

    let feeAmount = estimateTransactionFees(utxos.length, numOutputs, fees);

    // Calculate total utxo amount (satoshis)
    let totalAmount = new BigNumber(0);
    for (var i = 0; i < utxos.length; i++) {
        totalAmount = totalAmount.plus(utxos[i].amount);
    }

    
    // Calculate total fixed output amounts (satoshis)
    let fixedOutputSum = new BigNumber(0);
    for (var i = 0; i < fixedOutputs.length; i++) {
        fixedOutputSum = fixedOutputSum.plus(fixedOutputs[i].amount);
    }

    let remainingAmount = totalAmount.minus(fixedOutputSum).minus(feeAmount);

    fixedOutputs.push({"address": remainingAddress, "amount": remainingAmount});

    return fixedOutputs;
    
}

let myexports = { finalizeOutputs };

(function(exports){
})(typeof exports === 'undefined'? this['transactions']=myexports: myexports);

if (typeof module.exports === 'object') module.exports = myexports;
