function makeTokenizer(flow) {
  return function tokenizer(text) {
    let state = 0;
    let content = '';
    let at = 0;
    let to = 0;
    let tokens = [];
    text += '\0';
    const managers = flow[0];
    const actions = flow[1];
    for (let charIndex = 0; charIndex < text.length; charIndex++) {
      let char = text[charIndex];
      while (char !== null) {
        const manager = managers[state];
        const handlers = manager[0];
        let action_index = manager[1];
        for (let handlerIndex = 0; handlerIndex < handlers.length; handlerIndex++) {
          const handler = handlers[handlerIndex];
          if (handler[0].indexOf(char) !== -1) {
            action_index = handler[1];
            break;
          }
        }
        if (action_index === null) {
          throw new SyntaxError('action not defined on ' + state + ' with "' + char + '"');
        }
        let action = actions[action_index];
        const params = action[0];
        const options = params[0];
        const build = params[1];
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