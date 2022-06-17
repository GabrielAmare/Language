export default function makeTokenizer(managers) {
  return function tokenizer(text) {
    let state = 0;
    let content = '';
    let at = 0;
    let to = 0;
    let tokens = [];
    for (let char of text + '\0') {
      while (char !== null) {
        const manager = managers[state];
        let action = manager[1];
        for (const handler of manager[0]) {
          if (handler[0].includes(char)) {
            action = handler[1];
            break;
          }
        }
        if (!action) {
          throw new SyntaxError();
        }
        const [options, build] = action[0];
        if (!!(1 & options)) // add
          content += char;
        if (!!(2 & options)) // inc
          to++
        if (!!(4 & options)) // clr
          char = null;
        if (build) { // build
          let token = {type: build, content: content, at: at, to: to};
          tokens.push(token)
        }
        if (!!(8 & options)) { // clear
          content = '';
          at = to;
        }
        state = action[1];
      }
    }
    return tokens;
  }
}

