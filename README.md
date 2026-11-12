# 🧵📌🤖 Topic Shortcuts

A plugin for Nagram XF. Every topic of your forum groups gets its own launcher shortcut, with the topic's own name and icon, and tapping it opens that exact topic. Every bot you chat with gets one too, with its name and avatar. Long press the app icon, search for them in your launcher, put them as chips on a Nova Now card, or pin them to your home screen.

## Why I made it

I run a forum group with a topic per project. Nagram XF, like Telegram, publishes one shortcut per chat, so the whole group shows up as a single shortcut named after whichever topic spoke last, and it opens the group, not the topic. I wanted one shortcut per topic, the way I use them.

## What it does

* One shortcut per topic of every forum group you own or run, named after the topic, with its emoji icon (or its colored letter icon), opening that topic directly.
* Every bot chat in your chat list gets a shortcut too, named after the bot, with its avatar, opening that chat, in chat list order (can be switched off). Nagram XF only keeps the chats you have scrolled to in memory, so the plugin loads up to three more pages of your chat list once per start to find bots further down.
* Pinned topics come first, in their pinned order. Topics you name in the setting "Put these topics last" (General, Updates and Usage by default) go to the end.
* Android allows an app 15 dynamic shortcuts at once on a Pixel. A shortcut your launcher keeps (a Nova Now chip, a home screen icon) no longer needs one of those slots, so the plugin gives the slots to topics and bots that are not kept yet first, topics before bots, in the order of your chat list. That way every topic and bot reaches your launcher, and the kept ones stay current. With more than 15 not kept yet, the rest get a slot on the next pass after your launcher keeps the first ones.
* The settings screen lists every topic and bot under "Pin to home screen": tap one to place it on your home screen.

## Topic and bot chips on a Nova Now card

Nova Launcher's Nova Now page, left of your first home screen, shows cards. A card you build for Nagram XF shows only what you put in it: its featured shortcut (New conversation) and its actions. Nova never fills the actions in by itself, so a fresh card shows New conversation and nothing else.

To get a chip per topic or bot:

1. On the Nova Now page, tap the card's menu, then Settings.
2. Under Actions, tap Add action, open the Shortcuts tab and search for Telegram (Nagram XF's shortcuts carry that name).
3. Tick your topics and bots and tap Add, then Save.

Each chip opens its topic or bot chat. Nova pins every shortcut it keeps on a card, so the chips keep working even when one falls outside the 15 shortcuts Android lets the app publish at once, and the plugin keeps their names and icons current.

The card editor stops at six actions, but the card itself shows more. With root, `tools/nova_card_chips.py` writes any number of chips into the card (instructions at the top of the file). I run eleven topics and sixteen bots on mine.

## Performance

All work runs on the plugin queue, never on the UI thread: once a few seconds after start, when the app goes to the background, and after Nagram XF rebuilds its own shortcuts. Nothing is sent to Android when nothing changed, and pinned shortcuts are rebuilt only when a name or icon changed. No polling, no timers, no per message work. The extra chat list pages are asked for at most three times per start, the same request the app makes when you scroll down. Icons come from emoji and avatar files the app already has on disk; a bot avatar that is not on disk yet is fetched once at low priority and used on the next pass.

## Install

1. Use the plugin build of Nagram XF and turn on the plugin engine (Settings, N Settings, Plugins).
2. Download `topic_shortcuts.plugin` from the latest release.
3. Send it to your Saved Messages, tap it and choose install.

## How it works

The shortcuts open `LaunchActivity` with the action `com.tmessages.openchat...` and the extras `chatId` and `topicId`, the same extras a topic notification tap uses, so the app opens the topic itself (loading it first if it is not cached). They are long lived conversation shortcuts with a person and a locus id, published with `ShortcutManagerCompat`. Logcat tag `TopicShortcuts`.

## Tested

Nagram XF 12.10.1 plugin build on a Pixel 6 Pro with my real forum group (12 topics): 12 shortcuts published with the right names and icons, and the shortcuts for Deb and WSL2 each opened that topic, starting from a different topic. Then installed on my Pixel 8 Pro, where all 12 were published.

1.1.0 with Nova Launcher 8.9.7 on the Pixel 6 Pro: a Nagram XF card on the Nova Now page with six chips added through the card editor, then twelve written with the tool. Every chip showed its topic name and icon, and the Deb, Usage, GLaDOS and WSL2 chips each opened their topic. With the plugin forced to publish only six shortcuts, the six pinned ones outside that set were refreshed and still opened.

1.2.0 on the Pixel 6 Pro: the plugin found 13 bot chats, and a card with 12 topics and 13 bots showed every chip with its avatar; the DocMaker, ZLibrary and BotFather chips each opened that bot chat, and all 25 shortcuts were pinned by Nova. On my Pixel 8 Pro the plugin found 16 bots after loading more of the chat list (4 before), and the card there got all 16 after my topics.

Not tested by me: a pinned home screen shortcut and Nova's search results. They use the same intent as the tested chips.

## License

MIT

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=firestarter1996/xf-topic-shortcuts&type=Date)](https://star-history.com/#firestarter1996/xf-topic-shortcuts&Date)
