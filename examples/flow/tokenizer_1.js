import makeTokenizer from "../../tools/flow/tokenizer/portable.js";

// Import the json tokenizer structure
import struct from './tokenizer_1.json';

// create the tokenize function
let tokenize = makeTokenizer(struct);

// get your source text
let src = "1 + 23 * 45 - 67 / 890";

// tokenize it !
for (let token of tokenize(src)) {
  console.log(token);
}