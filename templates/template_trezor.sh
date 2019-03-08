# Enter the BIP32 path for the key with which you are signing.

path="ENTER PATH HERE"

# Define output and change address
outputamount=123456.7890
outputaddress="OUTPUTADDRESS"
changeaddress="CHANGEADDRESS"

# Define file names
inputsfile="./INPUTFILENAME.json"
outputsfile="./OUTPUTFILENAME.json"
sigfile1="./MY_SIGNATURE_FILENAME.json"
sigfile2="./OTHER_SIGNER_FILENAME.json"

# Your RedeemScript:
redeemscript="REDEEM_SCRIPT"

# Your Multisig Address:
multisigaddress="VAULT ADDRESS"

# All signers need to use identical inputs files.
# If you are the second signer, confirm that your file is identical to
# the first signer, or just use their file
./pymultisig/get_utxo_set.py $multisigaddress  --testnet > $inputsfile

# All signers need to use identical outputs files.
./pymultisig/generate_outputs.py $outputaddress $inputsfile > $outputsfile

# My Signature
./pymultisig/sign_multisig_spend.py $path $multisigaddress $redeemscript $inputsfile $outputsfile --testnet > $sigfile1

# If you are the second signer, or have both signarure files,
# Generate fully signed transaction ready for broadcasting
# Remove --testnet flag for mainnet transactions
./pymultisig/construct_signed_transaction.py $redeemscript $sigfile1 $sigfile2 $inputsfile $outputsfile --testnet
