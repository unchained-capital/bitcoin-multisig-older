#!/usr/bin/env node

const bitcoin          = require('bitcoinjs-lib');
const JSONbig          = require('json-bigint');
const BigNumber        = require('bignumber.js');
const fs               = require('fs');


// Command Line Script Interface
if (require.main === module) {
    var program = require('commander');

    program
        .version('0.1.0','-v, --version')
        .arguments('<redeemScript> <sigFile1> <sigFile2> <inputsFile> <outputsFile>')
        .option('--testnet', 'Generate Testnet Address (boolean)')
        .action(async function(redeemScript, sigFile1, sigFile2, inputsFile, outputsFile, options) {
            if (!options.testnet) {
                options.testnet = false;
            }

            let result = construct_signed_transaction(redeemScript,
                                                      [sigFile1, sigFile2],
                                                      inputsFile,
                                                      outputsFile,
                                                      options.testnet);
            console.log(result);
        })
        .parse(process.argv);
}

function construct_signed_transaction(redeemScript,
                                      sigFiles,
                                      inputsFile,
                                      outputsFile,
                                      testnet) {

    if (sigFiles.length != 2) {
        throw "Two Signature Files are Required"
    }

    // Load files
    var inputs = JSONbig.parse(fs.readFileSync(inputsFile, 'utf8'));
    
    var outputs = JSONbig.parse(fs.readFileSync(outputsFile, 'utf8'));

    var signatures = [];
    for (var i = 0; i < sigFiles.length; i++) {
        signatures[i] = JSONbig.parse(fs.readFileSync(sigFiles[i], 'utf8'));
    }


    // Order Signatures
    let parsedRedeemScript = bitcoin.payments.p2ms({output: Buffer.from(redeemScript,'hex')});
    let pubKeys = parsedRedeemScript.pubkeys.map(x => x.toString('hex'))

    let sigIndex1 = pubKeys.indexOf(signatures[0].pubkey)
    let sigIndex2 = pubKeys.indexOf(signatures[1].pubkey)
    if (sigIndex1 > sigIndex2) {
        signatures = [signatures[1], signatures[0]]
    }

    // Construct ScriptSigs
    var scriptSigs = [];
    var sigString;
    var inBuffer;
    for (var i = 0; i < inputs.length; i++) {
        sigString = "OP_0 " + signatures[0].signatures[i] + "01 " + signatures[1].signatures[i] + "01"
        inBuffer = bitcoin.script.fromASM(sigString);
        scriptSigs[i] = bitcoin.payments.p2sh({redeem: bitcoin.payments.p2ms({output: Buffer.from(redeemScript,'hex'),
                                            input: inBuffer
                                                                            })})
    }

    // Initial Transaction
    let transaction = new bitcoin.TransactionBuilder();
    transaction.setVersion(1);    
    if (testnet) {
        transaction.network = bitcoin.networks.testnet;
    }

    // OUTPUTS
    for (var i = 0; i < outputs.length; i++) {
        transaction.addOutput(outputs[i].address, outputs[i].amount)
    }

    // INPUTS
    for (var i = 0; i < inputs.length; i++) {
        transaction.addInput(inputs[i].txid, inputs[i].n)
    }

    var built = transaction.buildIncomplete()

    for (var i = 0; i < inputs.length; i++) {
        built.ins[i].script = scriptSigs[i].input
    }
    
    return built.toHex()
    
}
