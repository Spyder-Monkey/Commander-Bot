import discord
from discord.ext import commands


# Dec -> Bin
# Dec -> Hex
# Dec -> shits
# Dec -> Octal

# Bin -> Dec
# Bin -> Hex
# Bin -> Shits
# Bin -> Octal

# Hex -> Dec
# Hex -> Bin
# Hex -> Shits
# Hex -> Octal



class Conversions(commands.Cog):

    @commands.command(name="convert")
    async def convert(self, ctx, number, base: str=None):
        #            Binary      Hex         Octal        Decimal
        prefixes = {'0b':False, '0x':False, '0o': False, '':True}
        input_pre = number[0:2]
        for key in prefixes.keys():
            if input_pre == key:
                prefixes[key] = True
                prefixes[''] = False
                break

        if base == None:
            # Default. Get all conversions
            # Convert from decimal
            if prefixes['']: 
                await ctx.channel.send(self.dec_conversion(number))
            # Convert from binary
            elif prefixes['0b']:
                await ctx.channel.send(self.bin_conversion(number))
            # Convert from hex
            elif prefixes['0x']:
                await ctx.channel.send(self.hex_conversion(number))
            # Convert from octal
            elif prefixes['0o']:
                await ctx.channel.send(self.oct_conversion(number))
        elif base == '2':
            # Convert input number to binary
            if prefixes['']: 
                await ctx.channel.send("{} -> {}".format(number, int(number, 2)))
            # Convert from binary
            elif prefixes['0b']:
                await ctx.channel.send("Why would you ever want to convert binary to binary? Just drop out.")
            # Convert from hex
            elif prefixes['0x']:
                await ctx.channel.send("{} -> {}".format(number, bin(int(number, 16))))
            # Convert from octal
            elif prefixes['0o']:
                await ctx.channel.send("{} -> {}".format(number, bin(int(number, 8))))
        elif base == '8':
            # Convert input number to octal
            if prefixes['']: 
                await ctx.channel.send("{} -> {}".format(number, int(number, 8)))
            # Convert from binary
            elif prefixes['0b']:
                await ctx.channel.send("{} -> {}".format(number, oct(int(number, 2))))
            # Convert from hex
            elif prefixes['0x']:
                await ctx.channel.send("{} -> {}".format(number, oct(int(number, 16))))
            # Convert from octal
            elif prefixes['0o']:
                await ctx.channel.send("Why would you ever want to convert octal to octal? Just drop out.")
        elif base == '10':
            # Convert input number to decimal
            if prefixes['']: 
                await ctx.channel.send("Why would you ever want to convert decimal to decimal? Just drop out.")
            # Convert from binary
            elif prefixes['0b']:
                await ctx.channel.send("{} -> {}".format(number, int(number, 2)))
            # Convert from hex
            elif prefixes['0x']:
                await ctx.channel.send("{} -> {}".format(number, int(number, 16)))
            # Convert from octal
            elif prefixes['0o']:
                await ctx.channel.send("{} -> {}".format(number, int(number, 8)))
            
        elif base == '16':
            # Convert input number to hex
            if prefixes['']: 
                await ctx.channel.send("{} -> {}".format(number, int(number, 16)))
            # Convert from binary
            elif prefixes['0b']:
                await ctx.channel.send("{} -> {}".format(number, hex(int(number, 2))))
            # Convert from hex
            elif prefixes['0x']:
                await ctx.channel.send("Why would you ever want to convert hex to hex? Just drop out.")
            # Convert from octal
            elif prefixes['0o']:
                await ctx.channel.send("{} -> {}".format(number, hex(int(number, 8))))
        else:
            # ERROR
            await ctx.channel.send("Make sure the format is $convert <number> <base>.")

    """ DECIMAL CONVERSIONS """
    def dec_conversion(self, input):
        if input.isdecimal():
            response = "Decimal: {}\n----------------\nBinary: {}\nHex: {}\nOct: {}".format(input, bin(int(input)), hex(int(input)), oct(int(input)))
            return response
        else:
            return "Your input was not a base 10 number."
    """ BINARY CONVERSIONS """
    def bin_conversion(self, input):
        # Check if the string contains only 1's and 0's
        if all(c in '01' for c in input):
            response = "Binary: {}\n------------\nDecimal: {}\nHex: {}\nOct: {}".format(input, int(input, 2), hex(int(input, 2)), oct(int(input, 2)))
            return response
        else:
            return "Make sure you entered a base 2 number."
    """ HEX CONVERSIONS """
    def hex_conversion(self, ctx, input):
        response = ""
        return response
    """ OCTAL CONVERSIONS """
    def oct_conversion(self, ctx, input):
        decimal = int(input, 8)
        response = "Octal: {}\n---------------\nDecimal: {}\nBinary: {}\nHex: {}".format(input, decimal, bin(decimal), hex(decimal))
        return response





    """ SHIT CONVERSIONS """
    # Gigashart conversion
    @commands.command(name="gigashart")
    async def gigashart(self, ctx):
        # 1 bit = 69 shits
        # 420 shits = 1 shart

        # shit -> base 69
        # values [0-9] = [0-9]
        # values [10-36] = [a-z]
        # values [37-63] = [A-Z]
        # values [64-69] = [!, @, #, $, &]
        ctx.channel.send("This command still needs to be implemented.")

def setup(bot):
    bot.add_cog(Conversions(bot))