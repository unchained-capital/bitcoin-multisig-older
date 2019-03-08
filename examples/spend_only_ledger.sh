# The example below was generate with this set of 24 wallet words:
# merge alley   lucky   axis penalty manage latin   gasp  virus    captain wheel deal
# chase fragile chapter boss zero    dirt   stadium tooth physical valve   kid   plunge

# if the package has not been installed, use `npm link` to symlink scripts
# if you don't want to symlink the scripts, refer to their location at ./bin/${script}.js

# Enter the BIP32 path for the key with which you are signing.

#path2="m/45'/1'/501'/200/26"
path3="m/45'/1'/502'/200/26"

# Define output and change address
outputamount=0.1
outputaddress="2NCcmVAirNBDTQYvecdDpKNJVdKJruwdUSZ"
changeaddress="2MyvsR5gizb6JHSECL6csBHwpW1wL8xqHp4"

# Define file names
inputsfile="./examples/inputs.json"
outputsfile="./examples/outputs.json"
sigfile1="./examples/my_signature.json"
sigfile2="./examples/other_signaure.json"

# Your RedeemScript:
redeemscript="5221026c76fc386b6c339577eea265242eb902df43155a0eaf23af1f96c5d9f2d10f63210329b59270b95c8478fa36e0cf6f474736513d4e0157626b762dca41729e7756c22102b5b79489d0e3810ef911bfde82aad7d65e6d5fb4147686139d291f66eefd964d53ae"

# Your Multisig Address:
multisigaddress="2NAy762TReQqjNbNLdh3sK7cnje4GA4UfoW"

# All signers need to use identical inputs files.
# For testing, you can use an old inputs file to sign transactions with spent inputs
# WARNING: Inputsfile cannot be automatically created once the transaction has been broadcast
#get_utxo_set $multisigaddress --testnet > $inputsfile

# All signers need to use identical outputs files.
#generate_outputs $outputaddress $inputsfile --change_address $changeaddress --amount $outputamount > $outputsfile

# You would uncomment this to create your signature file
# Signature 1 (Mine)
#sign_multisig_spend $path3 $multisigaddress $redeemscript $inputsfile $outputsfile --testnet > $sigfile1

# The other signer would uncomment this to create their signature file
# Signature 2 (Other)
#sign_multisig_spend $path2 $multisigaddress $redeemscript $inputsfile $outputsfile --testnet > $sigfile2

# Once you have both signature files,
# Generate fully signed transaction ready for broadcasting
construct_signed_transaction $redeemscript $sigfile1 $sigfile2 $inputsfile $outputsfile --testnet

# Expected Signed Transaction:
# TxID: 3787c0db3a07efcde897a41402d861633fffc9f178703750201e40988fcd0a63
# 0100000003cd7f49fa87761c2eafc16a933a18d06f9b492aa940cf22cc7efb177417abaf2300000000fdfe00004830450221008101e4027dc2966ede7436af3e2548eb722cd071d6ba4b569ba6db034b59cd24022044594c9c695fee8991281e0834e787aaff33cc344cb9759712a7c326691afb1501483045022100cdc534a32804b8e6ca97e214aac5f147c4a9cc92405f0afd7f5ab59835c1c191022036fcdf2d6e43148cfbcbf595fd639950cd5c8d0191064beba3fe184f89afe93f014c695221026c76fc386b6c339577eea265242eb902df43155a0eaf23af1f96c5d9f2d10f63210329b59270b95c8478fa36e0cf6f474736513d4e0157626b762dca41729e7756c22102b5b79489d0e3810ef911bfde82aad7d65e6d5fb4147686139d291f66eefd964d53aeffffffff648b22491a034cf9da5ff0b4b600a1604f1dc348c3c452823eb7fe91fa69282300000000fc004730440220283d2fe9905d5078c6ba0825115daf39a710fadd561e0a43a1a8c7d55952a3a30220120dcf52e5b11f3c43adc25ae63d40a11fdd0dbfdd5f1aafd7464ac0f8e1bfbc014730440220596250e1f4047442bf3e1b4c3a5d79d95711a8b43de20a6ecc283e83eb29fb98022040f9016465412f1f388f9e3462e1b976e635512d3b7d22092e734ed9bcee1e88014c695221026c76fc386b6c339577eea265242eb902df43155a0eaf23af1f96c5d9f2d10f63210329b59270b95c8478fa36e0cf6f474736513d4e0157626b762dca41729e7756c22102b5b79489d0e3810ef911bfde82aad7d65e6d5fb4147686139d291f66eefd964d53aeffffffffc2cc9c2614e53667b8a32e0b07b2fdb06aa1dec11ebd0c3468b1b229830034c500000000fdfe0000483045022100d34cebe8f5b205c503080aa6d582107a01428edadd15bdcdcbe789a6b259e2eb022049b17467982f1dadddc4c926b6214180a27cc069654c54cea24b94d2987becfe01483045022100a3dcd20584996321144d63a61dfef586b841cfc78a4ea0870e5c13858ceca1aa02200a0527d084da1252acae38ac5d39f165ec2773803b7b584a71a0b55bcdce0661014c695221026c76fc386b6c339577eea265242eb902df43155a0eaf23af1f96c5d9f2d10f63210329b59270b95c8478fa36e0cf6f474736513d4e0157626b762dca41729e7756c22102b5b79489d0e3810ef911bfde82aad7d65e6d5fb4147686139d291f66eefd964d53aeffffffff02809698000000000017a914d47d6b15df85155a705c83cc0777b1da7594b4a087f99fa7000000000017a9144950385c03dde552965cfe12e7a2edfdc0d1f9608700000000

