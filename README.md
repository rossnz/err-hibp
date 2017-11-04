# err-hibp

A plugin for [Errbot](http://github.com/gbin/err) that perform a lookup of an email address in the [HaveIBeenPwned](https://haveibeenpwned.com/) database.

I tried to keep this as simple as possible and it's working for me. Note that I use Slack so I may have biased output towards that - it's untested for any other backends (submit a PR if you'd like to change anything). Note that some email addresses can have a lot of hits, so I've hard coded a limit for max number of results to 20.

## Config

None required.

## License

GNU General Public License v2.0
