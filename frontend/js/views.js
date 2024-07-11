// Javascript Code for View count
const counter = document.querySelector(".counter-number");                                                      // query HTML class "counter-number"
const digitsContainer = document.querySelector(".counter-digits");                                              // Container for flip digits

async function updateCounter() {                                                                                // Create Function updateCounter()
    let response = await fetch("https://2hcmeqq4gbwopbikzrwbortf440bdeke.lambda-url.eu-west-2.on.aws/");        // Fetch Lambda function
    let data = await response.json();                                                                           // Store Lambda function in "data"                                          // Views = data from Lambda
    updateFlipCounter(data);
}

function updateFlipCounter(number) {
    const digits = number.toString().padStart(4, '0').split(''); // Ensure there are always 4 digits
    document.querySelectorAll('.digit').forEach((digit, index) => {
        const top = digit.querySelector('.top');
        const bottom = digit.querySelector('.bottom');
        const newDigit = digits[index];
        
        if (top.textContent !== newDigit) {
            bottom.textContent = newDigit;
            digit.classList.add('flip');
            
            setTimeout(() => {
                top.textContent = newDigit;
                digit.classList.remove('flip');
            }, 500);
        }
    });
}

updateCounter();