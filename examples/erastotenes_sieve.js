
const primes = [2,3];
let isPrime = false;
let stopfor = false;

for(let i = 4; i < 2000; i++) {
    isPrime = true;
    stopfor = false;
    
    for(let prime of primes) {
        if(!stopfor) {
            if(i % prime === 0) {
                isPrime = false;
                stopfor = true;
            }
        }

    }
    if(isPrime) {
        console.log(i, " is prime")
        primes.push(i);
    }
}