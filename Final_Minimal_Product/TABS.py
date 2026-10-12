"""Encode text with the original TABS models and variable bit widths."""

from Assisting_Files.Bascii import ENTABIS, DETABIS
from Assisting_Files.DecimalProcessing import endecimalprocessing, dedecimalprocessing


def EN_TABS(message, optimized=True, model_filename=False):
    if not isinstance(message, str):
        raise ValueError("The message must be text.")
    dec = ENTABIS(message=message, model_filename=model_filename,
                  bestmodel=True, includewordlists=optimized)
    if dec.check_error():
        raise ValueError("The model cannot encode every character in this message.")
    return endecimalprocessing(decimal=dec.givinglikesanta(),
                              check_bytelen=optimized, optimization=optimized).santa()


def DE_TABS(binary):
    dec = dedecimalprocessing(binarystring=binary).santa()
    return DETABIS(decimal_list=dec).givinglikesanta()


if __name__ == "__main__":
    message = "This is a safe demo message."
    binary = EN_TABS(message)
    print(f"TABS: {len(binary)} bits")
    print(DE_TABS(binary))
