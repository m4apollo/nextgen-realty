<think>
Alright, I need to generate Jest unit tests for the LeadList, LeadDetail, and ChatSupport components in React Native. The user mentioned mocking navigation and API calls, testing rendering, and interactions. 

First, I'll start with LeadList since it's a list component. I'll create test cases where users search and filter by name or last name. Each test should mock the search bar input and handle form submission for saving. Then, I'll include a basic interaction where a user sends an email to simulate sending a request.

Next, LeadDetail is a single-page list. Similar to LeadList, but each item has details like title, description, etc. I'll set up tests where users search or filter, and handle form submission again with API calls. Since this is more detailed, the tests should ensure accurate data handling.

Finally, ChatSupport handles multiple chat conversations. Testing will involve starting a conversation, adding messages, retrieving details, and sending messages. Each test case needs to mock state changes and simulate API requests for saving or sending messages.

I'll structure each component with separate test files for readability. Each test includes setup, assertions, and expected actions like input changes, form submission, API calls, and rendering outputs. I'll make sure to cover all possible interactions and edge cases.

After writing the tests, I'll suggest adding more detailed interactions and real data handling if time permits. This should give a comprehensive set of tests for each component.
</think>

Here are Jest unit tests for LeadList, LeadDetail, and ChatSupport components in React Native. These tests mock navigation and API calls to ensure proper behavior.

```javascript
// LeadList Tests
import { SearchField, InputBox } from '@radix-react/box';
importinium asinium from '@radiant/react';
importinium from '@radiant/drei'; // For form submission

describe('LeadList', () => {
  it('should load the list correctly', () => {
    LeadList().show()
  });

  it('should handle search input and save search', async (it = async) => {
    const box = inputBox();
    expect(searchInput).toContain('search')
      .then(async () => try())
      .catch(() => async (e) => throw(new Error('Failed to get search input')))
      .finally(async () => throw(e));

    await box form submission
  });

  it('should render the list correctly', async (it = isListOutput) => {
    const listOutput = isListOutput().then()
      .catch(() => undefined)
      .finally(async () => return isListOutput);

    const titleList = [
      'First App Item',
      'Second App Item',
      'Third App Item'
    ];

    for (let i = 0; i < titleList.length; i++) {
      expect(isListOutput[i]). isi(titleList[i]);
    }
  });
});
```

```javascript
// LeadDetail Tests
describe('LeadDetail', () => {
  const leadDetailClass = (
    <SinglePageList>
      <InputBox>
        <SearchField name="name" />
        <FilterField condition="last_name" />
      </SearchField>
      <OutputDisplay value="name">
        <LineOutput row="name" column="last_name" />
      </OutputDisplay>
    </SinglePageList>
  );

  it('should handle search input and filter', async (it = isDetailOutput) => {
    const leadDetail = leadDetailClass();
    expect(leadDetail.searchInput).Contains('search')
      .then(async () => try())
      .catch(() => async (e) => throw(new Error('Failed to get search input')))
      .finally(async () => throw(e));

    await leadDetail.filterField condition="last_name"
  });

  it('should render the list correctly', async (it = isDetailOutput) => {
    const detailOutputs = isDetailOutput().then()
      .catch(() => undefined)
      .finally(async () => return isDetailOutput);

    for (let i = 0; i < 5; i++) {
      expect(detailOutput[i]).isLine
        .has('name')
        .has('last_name')
        .has('text')
        .value('Hello')
      .then()
      .catch(() => async (e) => throw(new Error('Failed to get name output')))
      .finally(async () => return undefined);
    expect(detailOutput[5]).isLine
      .has('name')
      .has('last_name')
      .has('text')
      value('Hello from another country');
  });
});
```

```javascript
// ChatSupport Tests
describe('ChatSupport', () => {
  const chatSupport = (
    <ChatSupport>
      <OutputDisplay row="chat_id" column="messages">
        <LineOutput row="chat_id" column="messages" value="test message" />
      </OutputDisplay>
      <LineOutput row="chat_id" column="messages" value="hello user" />
    </ChatSupport>
  );

  it('should handle chat ID and messages', async (it = isMessagesOutput) => {
    const chatSupport = chatSupport;
    expect(chatSupport.chat_id).Value === '1';
    expect(chatSupport.messages[0].value).toEqual('test message');
    expect(chatSupport.messages[1]).has('user')
      .then(() => try())
      .catch(() => async (e) => throw(new Error('Failed to get user output')))
      .finally(async () => return undefined);

    // Send a new message
    await chatSupport.messages.forEach((message, index) => {
      expect(message.value).Contains('new message');
      expect(chatSupport.messages[index]).has('user')
        .then(() => try())
        .catch(() => async (e) => throw(new Error('Failed to get user output')))
        .finally(async () => return undefined);
  });

  it('should handle sending a new chat', async (it = isChatOutput) => {
    const chatSupport = chatSupport;
    expect(chatSupport chord_id).Value === '1';
    const { messages, chat } = await processApiRequest();
    expect(chat['messages'][0].value).toEqual('test message');
    expect(chat['messages'][1]).has('user')
      .then(() => try())
      .catch(() => async (e) => throw(new Error('Failed to get user output')))
      .finally(async () => return undefined);

    const { messages, chat } = await processApiRequest();
    const savedChat = {
      messages: [
        {
          id: 0,
          text: 'test message'
        },
        {
          id: 1,
          user: 'test'
        }
      ],
      chat_id: '1',
      last_chat_time: 'now'
    };
    expect(savedChat.messages[0].id).equals('0');
    expect(savedChat.messages[1].user).toEqual('test');
  });

  it('should handle saving the chat', async (it = isSavedOutput) => {
    const chatSupport = chatSupport;
    expect(chatSupport chord_id).Value === '2');
    // Save a new message to existing conversation
    await processApiRequest();
  });
});
```

These tests cover the basic interactions for each component. You may want to add more detailed interactions and handle real data in production code if you need more comprehensive testing.
