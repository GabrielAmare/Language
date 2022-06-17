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
        const params = action[0];
        if (params[0]) // add
          content += char;
        if (params[1]) // use
          to++
        if (params[2]) // clr
          char = null;
        if (params[3]) { // build
          let token = {type: params[3], content: content, at: at, to: to};
          tokens.push(token)
        }
        if (params[4]) { // clear
          content = '';
          at = to;
        }
        state = action[1];
      }
    }
    return tokens;
  }
}

