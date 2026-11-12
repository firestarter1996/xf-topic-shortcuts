# 🧵📌🧩 Topic Shortcuts

A plugin for Nagram XF. Every topic of your forum groups gets its own launcher shortcut, with the topic's own name and icon, and tapping it opens that exact topic. Long press the app icon, search for the topic in your launcher, put your topics as chips on a Nova Now card, or pin them to your home screen.

## Why I made it

I run a forum group with a topic per project. Nagram XF, like Telegram, publishes one shortcut per chat, so the whole group shows up as a single shortcut named after whichever topic spoke last, and it opens the group, not the topic. I wanted one shortcut per topic, the way I use them.

## What it does

* One shortcut per topic of every forum group you own or run, named after the topic, with its emoji icon (or its colored letter icon), opening that topic directly.
* Your recent bot chats that have no shortcut yet get one too (can be switched off).
* Pinned topics come first, in their pinned order. Topics you name in the setting "Put these topics last" (General, Updates and Usage by default) go to the end.
* Android shows a limited number of shortcuts per app (15 on a Pixel). When there are more topics than room, the settings screen lists every topic under "Pin to home screen": tap one to place it on your home screen, where it stays no matter how many there are.

## Topic chips on a Nova Now card

Nova Launcher's Nova Now page, left of your first home screen, shows cards. A card you build for Nagram XF shows only what you put in it: its featured shortcut (New conversation) and its actions. Nova never fills the actions in by itself, so a fresh card shows New conversation and nothing else.

To get a chip per topic:

1. On the Nova Now page, tap the card's menu, then Settings.
2. Under Actions, tap Add action, open the Shortcuts tab and search for Telegram (Nagram XF's shortcuts carry that name).
3. Tick your topics and tap Add, then Save.

Each chip opens its topic. Nova pins every shortcut it keeps on a card, so the chips keep working even when a topic falls outside the 15 shortcuts Android lets the app publish at once, and the plugin keeps their names and icons current.

The card editor stops at six actions, but the card itself shows more. With root, `tools/nova_card_chips.py` writes any number of chips into the card (instructions at the top of the file). I run twelve on mine.

## Performance

All work runs on the plugin queue, never on the UI thread: once a few seconds after start, when the app goes to the background, and after Nagram XF rebuilds its own shortcuts. Nothing is sent to Android when nothing changed, and pinned topic shortcuts are rebuilt only when a topic's name or icon changed. No polling, no timers, no per message work. Icons come from emoji files the app already has on disk.

## Install

1. Use the plugin build of Nagram XF and turn on the plugin engine (Settings, N Settings, Plugins).
2. Download `topic_shortcuts.plugin` from the latest release.
3. Send it to your Saved Messages, tap it and choose install.

## How it works

The shortcuts open `LaunchActivity` with the action `com.tmessages.openchat...` and the extras `chatId` and `topicId`, the same extras a topic notification tap uses, so the app opens the topic itself (loading it first if it is not cached). They are long lived conversation shortcuts with a person and a locus id, published with `ShortcutManagerCompat`. Logcat tag `TopicShortcuts`.

## Tested

Nagram XF 12.10.1 plugin build on a Pixel 6 Pro with my real forum group (12 topics): 12 shortcuts published with the right names and icons, and the shortcuts for Deb and WSL2 each opened that topic, starting from a different topic. Then installed on my Pixel 8 Pro, where all 12 were published.

1.1.0 with Nova Launcher 8.9.7 on the Pixel 6 Pro: a Nagram XF card on the Nova Now page with six chips added through the card editor, then twelve written with the tool. Every chip showed its topic name and icon, and the Deb, Usage, GLaDOS and WSL2 chips each opened their topic. With the plugin forced to publish only six shortcuts, the six pinned ones outside that set were refreshed and still opened.

Not tested by me: a pinned home screen shortcut and Nova's search results. They use the same intent as the tested chips.

## License

MIT

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=firestarter1996/xf-topic-shortcuts&type=Date)](https://star-history.com/#firestarter1996/xf-topic-shortcuts&Date)
