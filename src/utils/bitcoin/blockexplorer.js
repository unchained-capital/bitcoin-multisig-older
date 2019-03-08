const fetch = require('node-fetch');

async function getUtxoSet(address, testnet) {
    let apiUrl;
    if (testnet) {
        apiUrl = "https://testnet.blockchain.info/";
    } else {
        apiUrl = "https://blockchain.info/";
    }
    
    const utxoPrefix = "unspent?cors=true&active=";
    var url_end = "?cors=true&format=hex";

    var res = await fetch(apiUrl + utxoPrefix + address);

    var utxos = await res.json();

    var outputs = utxos.unspent_outputs.map(utxo => ({txid: utxo.tx_hash_big_endian,
                                                       n: utxo.tx_output_n,
                                                       amount: utxo.value}));
    var final_outputs = await outputs.map(async (o) => {
        res = await fetch(apiUrl+"tx/"+o.txid+url_end);
        o.rawreftx = await res.text();
        return o;
    });

    return Promise.all(final_outputs);
}


let myexports = { getUtxoSet };

(function(exports){
})(typeof exports === 'undefined'? this['blockexplorer']=myexports: myexports);

if (typeof module.exports === 'object') module.exports = myexports;
