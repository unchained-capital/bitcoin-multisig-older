const bitcoin = require('bitcoinjs-lib');

const TransportU2F = require("@ledgerhq/hw-transport-u2f").default;
const LedgerBtc    = require("@ledgerhq/hw-app-btc").default;

const { compressPublicKey, generateMultisigAddress } = require('./btc_utils');

async function exportLedgerPubKey(path, ledgerbtc) {
    const result = await ledgerbtc.getWalletPublicKey(path, true);
    const compressedPublicKey = compressPublicKey(result.publicKey);
    return compressedPublicKey;    
};


async function browserExportLedgerPubKey(path) {
    const transport = await TransportU2F.create();
    const ledgerbtc = new LedgerBtc(transport);
    return exportLedgerPubKey(path, ledgerbtc);
}   


async function signMultisigSpendLedger(path,
                                       address,
                                       redeemScript,
                                       inputs,
                                       outputs,
                                       testnet,
                                       ledgerbtc) {

    // Verify that Pubkeys and Address match
    var checkAddress = generateMultisigAddress(redeemScript, testnet);

    if (address !== checkAddress) {
        throw new Error("Incorrect Redeem Script");
    }

    let ledgerInputs = []; // array[tx, index, redeemscript]

    // OUTPUTS
    let outputTmp = new bitcoin.TransactionBuilder();
    outputTmp.setVersion(1);
    if (testnet) {
        outputTmp.network = bitcoin.networks.testnet;
    }

    for (var i = 0; i < outputs.length; i++) {
        // the parseInt is so that this can accept Ints or BigNumbers
        outputTmp.addOutput(outputs[i].address, parseInt(outputs[i].amount.toString(), 10));
    }
    let outputTmpHex = outputTmp.buildIncomplete().toHex();
    
    let outputTx = await ledgerbtc.splitTransaction(outputTmpHex);
    let outputScriptHex = await ledgerbtc.serializeTransactionOutputs(outputTx).toString('hex');

    // INPUTS - assumes all inputs have the same address
    let splitTx;
    for (var j = 0; j < inputs.length; j++) {
        splitTx = await ledgerbtc.splitTransaction(inputs[j].rawreftx, true);
        ledgerInputs[j] = [splitTx, inputs[j].n, redeemScript];
    }

    // BIP32 PATH
    let ledger_bip32_path = path.split("/").splice(1).join("/");
    let ledgerKeySets = Array(inputs.length).fill(ledger_bip32_path); //array[bip32]

    // SIGN
    let pubkey = await exportLedgerPubKey(path, ledgerbtc);
    
    let signatures = await ledgerbtc.signP2SHTransaction(
        ledgerInputs,
        ledgerKeySets,
        outputScriptHex
    );

    let result = {pubkey: pubkey, signatures: signatures};

    return result;
}

async function browserSignMultisigSpendLedger(path,
                                              address,
                                              redeemScript,
                                              inputs,
                                              outputs,
                                              testnet) {
    const transport = await TransportU2F.create();
    const ledgerbtc = new LedgerBtc(transport);
    return signMultisigSpendLedger(path,
                                   address,
                                   redeemScript,
                                   inputs,
                                   outputs,
                                   testnet,
                                   ledgerbtc);
}   



let myexports = { exportLedgerPubKey,
                  browserExportLedgerPubKey,
                  browserSignMultisigSpendLedger,
                  signMultisigSpendLedger };

(function(exports){
})(typeof exports === 'undefined'? this['ledger']=myexports: myexports);

if (typeof module.exports === 'object') module.exports = myexports;
