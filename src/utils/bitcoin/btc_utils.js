const bitcoin = require('bitcoinjs-lib');


function validateHex(inputString) {
    if (inputString.length % 2) {
        throw new Error("invalid hex - odd-length string");
    }
    var re = /^[0-9A-Fa-f]*$/;
    if (!re.test(inputString)) {
        throw new Error("invalid hex - invalid characters");
    }
}



function compressPublicKey(publicKey) {
    validateHex(publicKey);
    //validate Public Key Length
    //validate Public Key Structure
    let pubkey_buffer = Buffer.from(publicKey, 'hex');
    let prefix = (pubkey_buffer[64] & 1) !== 0 ? 0x03 : 0x02;
    let prefixBuffer = Buffer.alloc(1);
    prefixBuffer[0] = prefix;
    return Buffer.concat([prefixBuffer, pubkey_buffer.slice(1, 1 + 32)]).toString('hex');
}

function generateMultisigRedeemScript(pubkey1, pubkey2, pubkey3) {
    let pubkeys = [pubkey1, pubkey2, pubkey3
                  ].map((hex) => Buffer.from(hex, 'hex'));

    let redeem = bitcoin.payments.p2ms({ m: 2, pubkeys });

    return redeem.output.toString('hex');
}

function generateMultisigAddress(redeemScript, testnet) {
    let net;
    if (testnet) {
        net = bitcoin.networks.testnet;
    } else {
        net = bitcoin.networks.bitcoin;
    }

    let redeemP2MS = bitcoin.payments.p2ms({output: Buffer.from(redeemScript, 'hex'),
                                            network: net});

    let { address } = bitcoin.payments.p2sh({
        redeem: redeemP2MS,
        network: net
    });

    return address;
}

function extractPublicKeysHex(redeemScript) {
    let parsedRedeemScript = bitcoin.payments.p2ms(
        {output: Buffer.from(redeemScript,'hex')}
    );        
    let pubKeysHex = parsedRedeemScript.pubkeys.map(x => x.toString('hex'));
    // validate M and N?
    return pubKeysHex;
}
    


function estimateTransactionFees(numInputs, numOutputs, feesPerByteInSatoshis) {
    /*
      Estimate total transaction fee for non-segwit, 2-of-3 P2SH-multisig UTXO spends

      Fee estimation is based of the following encoding assumptions
      10 Overhead bytes:
      version - 4
      input count - 1
      output count - 1
      locktime - 4
      
      297 Bytes per 2/3-multisig utxo:
      prev_tx - 32
      index -4
      scriptsize - 3
      scriptsig - 254
      sequence - 4
      
      34 Bytes per output (conservative assuming P2PKH)

      Args:
      num_inputs: number of UTXOs being spent
      num_outputs: number of outputs
      fees_per_byte_in_satoshis:

      Returns:
      Total transaction fee in satoshis

      Example:
      TODO
    */
    
    let txLengthInBytes = 10 + (297 * numInputs) + (34 * numOutputs);

    let feesInSatoshis   = txLengthInBytes * feesPerByteInSatoshis;

    return feesInSatoshis;
}




let myexports = { compressPublicKey,
                   estimateTransactionFees,
                   generateMultisigRedeemScript,
                   generateMultisigAddress,
                   extractPublicKeysHex };

(function(exports){
})(typeof exports === 'undefined'? this['btcUtils']=myexports: myexports);

if (typeof module.exports === 'object') module.exports = myexports;
