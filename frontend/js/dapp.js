// Change this address to match your deployed contract!
const contract_address = "0x9aEd2D95a6c52b0076bd0Ca9646B5F17d009b209";


const dApp = {
  ethEnabled: function() {
    // If the browser has MetaMask installed
    if (window.ethereum) {
      window.web3 = new Web3(window.ethereum);
      window.ethereum.enable();
      return true;
    }
    return false;
  },
  updateUI: function() {
    const renderItem = (copyright_id, reference_uri, icon_class, {name, vintage, origin, producer, appraisal_value, possessor, owner, image}) => `
        <li>
          <div class="collapsible-header"><i class="${icon_class}"></i>Copyright Number ${copyright_id}: ${name}</div>
          <div class="collapsible-body">
            <h6>Description</h6>
            <p>${vintage}</p>
            <p>${origin}</p>
            <p>${producer}</p>
            <p>${appraisal_value}</p>
            <p>${possessor}</p>
            <p>${owner}</p>
            <img src="https://gateway.pinata.cloud/ipfs/${image.replace("ipfs://", "")}" style="width: 100%" />
            <p><a href="${reference_uri}">Reference URI</a></p>
          </div>
        </li>
    `;

    // fetch json metadata from IPFS (name, description, image, etc)
    const fetchMetadata = (reference_uri) => fetch(`https://gateway.pinata.cloud/ipfs/${reference_uri.replace("ipfs://", "")}`,
     { mode: "cors" }).then((resp) => resp.json());

    // fetch the Copyright Events from the contract and append them to the UI list
    this.contract.events.Copyright({fromBlock: 0}, (err, event) => {
      const { copyright_id, reference_uri } = event.returnValues;

      fetchMetadata(reference_uri)
      .then((json) => {
        $("#dapp-copyrights").append(renderItem(copyright_id, reference_uri, "far fa-copyright", json));
      });
    });

    // fetch the OpenSource Events from the contract and append them to the UI list
    this.contract.events.OpenSource({fromBlock: 0}, (err, event) => {
      const { copyright_id, reference_uri } = event.returnValues;

      fetchMetadata(reference_uri)
      .then((json) => {
        $("#dapp-opensource").append(renderItem(copyright_id, reference_uri, "fab fa-osi", json));
      });
    });
  },
  copyrightWork: async function() {
    const name = $("#dapp-copyright-name").val();
    const vintage = $("#dapp-copyright-vintage").val();
    const origin = $("#dapp-copyright-origin").val();
    const producer = $("#dapp-copyright-producer").val();
    const appraisal_value = $("#dapp-copyright-appraisal_value").val();
    const possessor = $("#dapp-copyright-possessor").val();
    const owner = $("#dapp-copyright-owner").val();
    const image = document.querySelector('input[type="file"]');

    const pinata_api_key = $("#dapp-pinata-api-key").val();
    const pinata_secret_api_key = $("#dapp-pinata-secret-api-key").val();

    if (!pinata_api_key || !pinata_secret_api_key || !name || !vintage || !origin || !producer || !appraisal_value || !possessor || !owner || !image) {
      M.toast({ html: "Please fill out the entire form!" });
      return;
    }

    const image_data = new FormData();
    image_data.append("file", image.files[0]);
    image_data.append("pinataOptions", JSON.stringify({cidVersion: 1}));

    try {
      M.toast({ html: "Uploading Image to IPFS via Pinata..." });
      const image_upload_response = await fetch("https://api.pinata.cloud/pinning/pinFileToIPFS", {
        method: "POST",
        mode: "cors",
        headers: {
          pinata_api_key,
          pinata_secret_api_key
        },
        body: image_data,
      });

      const image_hash = await image_upload_response.json();
     
      const image_uri = `ipfs://${image_hash.IpfsHash}`;

      M.toast({ html: `Success. Image located at ${image_uri}.` });
      M.toast({ html: "Uploading JSON..." });

      const reference_json = JSON.stringify({
        pinataContent: { name: name, vintage: vintage, origin: origin, producer: producer, appraisal_value: appraisal_value, possessor: possessor, owner: owner, image: image_uri },
        pinataOptions: {cidVersion: 1}
      });
    
      const json_upload_response = await fetch("https://api.pinata.cloud/pinning/pinJSONToIPFS", {
        method: "POST",
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
          pinata_api_key,
          pinata_secret_api_key
        },
        body: reference_json
      });

      const reference_hash = await json_upload_response.json();
      const reference_uri = `ipfs://${reference_hash.IpfsHash}`;
      $("#reference-uri").html(reference_uri);
      alert(reference_uri);

      M.toast({ html: `Success. Reference URI located at ${reference_uri}.` });
      M.toast({ html: "Sending to blockchain..." });

      if ($("#dapp-opensource-toggle").prop("checked")) {
        this.contract.methods.OpenSourceWork(reference_uri).send({from: this.accounts[0]})
        .on("receipt", (receipt) => {
          alert("tranasction hash", receipt)
          M.toast({ html: "Transaction Mined! Refreshing UI..." });
          location.reload();
        });
      } else {
        this.contract.methods.copyrightWork(reference_uri).send({from: this.accounts[0]})
        .on("receipt", (receipt) => {
          M.toast({ html: "Transaction Mined! Refreshing UI..." });
          location.reload();
        });
      }

    } catch (e) {
      alert("ERROR:", JSON.stringify(e));
      console.log(e)
    }
  },
  main: async function() {
    // Initialize web3
    if (!this.ethEnabled()) {
      alert("Please install MetaMask to use this dApp!");
    }

    this.accounts = await window.web3.eth.getAccounts();

    this.cryptoRightABI = await (await fetch("./CryptoRight.json")).json();

    this.contract = new window.web3.eth.Contract(
      this.cryptoRightABI,
      contract_address,
      { defaultAccount: this.accounts[0] }
    );
    console.log("Contract object", this.contract);

    this.updateUI();
  }
};

dApp.main();
