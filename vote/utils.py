from vote.models import VoteKey

def get_key(key_msg):
    try:
        print(key_msg)
        return VoteKey.objects.get(key=key_msg)
    except VoteKey.DoesNotExist:
        return None


def votekey_valid(key):
    return VoteKey.objects.filter(key=key).exists()