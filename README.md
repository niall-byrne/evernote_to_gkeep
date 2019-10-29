# evernote_to_gkeep

Export your notes from the Evernote App, and import them into Google Keep with this tool.

## Usage Example:

To upload all files in the `import` folder, run this command:

```
python main.py --directory import --username my_email@gmail.com --password mypassword
```

## Environment Variables:

You may specify your credentials using the following environment variables:

```
export GKEEP_USERNAME="my_email@gmail.com"
export GKEEP_PASSWORD="mypassword"
```

## Google Keep
This project uses [The Unofficial Google Keep API](https://github.com/kiwiz/gkeepapi), and thanks it's author for their hard work.
