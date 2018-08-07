def save(self, *args, **kwargs):
    if self.attachment_file:
        img = Img.open(self.attachment_file)

        if img.mode != 'RGB':
            img = img.convert('RGB')

        output = BytesIO()

        img.save(output, format='JPEG', quality=70)
        output.seek(0)

        self.attachment_file = InMemoryUploadedFile(output, 'ImageField', self.filename,
                                                    'image/jpeg', sys.getsizeof(output), None)

    return super(Attachment, self).save(*args, **kwargs)
