Relase Note for version 1.23.2.2.1
============================================================

これ以前のPython CAでWaveform レコードにputを繰り返すと、当初は正常に
動作しているが、2000-3000回程度を超えたところで、

  Fatal Python error: deallocating None

とのエラーメッセージを残して、プロセスがクラッシュするという現象が発生することが判明した。

これに対応するために、:py:func:`Py_XDECREF` 呼び出しの際に参照回数を減らす対象のオブジェクト
が:py:class:`Py_None` で無いことをチェックするように _ca314.cpp を変更した。

:py:class:`Py_None` に対しても:py:func:`Py_INCREF` を呼んでおり、:py:class:`Py_None` に対して:py:func:`Py_DECREF` を呼んだ場合、
いつでもクラッシュする訳ではないようなので、完全には理解できていないが、クラッシュすることは
なくなった。 :py:class:`Py_None` に対して :py:func:`Py_DECREF` 呼び出しをかけようとした時にメッセージを出す様にしてもこのメッセージは表示されない。

