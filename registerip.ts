import { PIL_TYPE } from '@story-protocol/core-sdk';
import { toHex, Address, zeroAddress } from 'viem';

async function registerIp(client: any) {
    const newCollection = await client.nftClient.createNFTCollection({
        name: 'Test NFT',
        symbol: 'TEST',
        isPublicMinting: true,
        mintOpen: true,
        mintFeeRecipient: zeroAddress,
        contractURI: '',
        txOptions: { waitForTransaction: true },
    });

    const response = await client.ipAsset.mintAndRegisterIp({
        spgNftContract: newCollection.spgNftContract as Address,
        ipMetadata: {
            ipMetadataURI: 'test-uri',
            ipMetadataHash: toHex('test-metadata-hash', { size: 32 }),
            nftMetadataHash: toHex('test-nft-metadata-hash', { size: 32 }),
            nftMetadataURI: 'test-nft-uri',
        },
        txOptions: { waitForTransaction: true }
    });

    console.log(`Completed at transaction hash ${response.txHash}, NFT Token ID: ${response.tokenId}, IPA ID: ${response.ipId}, License Terms ID: ${response.licenseTermsId}`);
}

export default registerIp;